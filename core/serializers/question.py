from rest_framework import serializers

from ..models import Question, DirectIndicator, AnswerOption
from .answer_option import AnswerOptionSerializer
from .direct_indicator2 import DirectIndicatorSerializer2


class QuestionSerializer(serializers.ModelSerializer):
    uiComponent = serializers.ChoiceField(choices=Question.UI_COMPONENT_TYPES)
    direct_indicator = DirectIndicatorSerializer2(many=True)
    section_name = serializers.ReadOnlyField(source='section.title')

    class Meta:
        model = Question
        fields = [
        'id',
        'method',
        'topic',
        'section',
        'section_name',
        'order', 
        'isMandatory', 
        'name', # R
        'description', 
        'instruction', 
        'uiComponent',  # R
        'direct_indicator'
        ]
    
    def create(self, validated_data): 
        direct_indicator_data = validated_data.pop('direct_indicator')
        
        print(direct_indicator_data)
        question = Question.objects.create(**validated_data)
        if len(direct_indicator_data):
            direct_indicator_data = direct_indicator_data[0]
            directIndicator = DirectIndicator.objects.create(question=question, method=validated_data['method'], **direct_indicator_data)
            options = direct_indicator_data.pop('options')
       
            for option in options:
                option_instance, _ = AnswerOption.objects.get_or_create(order=option.get('order', 1), text=option['text'])
                directIndicator.options.add(option_instance.id)
        return question

    def update(self, instance, validated_data):
        print(validated_data)
        direct_indicator_data = validated_data.pop('direct_indicator')
        instance.method = validated_data.get('method', instance.method)
        instance.topic = validated_data.get('topic', instance.topic)
        instance.section = validated_data.get('section', instance.section)
        instance.order = validated_data.get('order', instance.order)
        instance.isMandatory = validated_data.get('isMandatory', instance.isMandatory)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.instruction = validated_data.get('instruction', instance.instruction)
        instance.uiComponent = validated_data.get('uiComponent', instance.uiComponent)
        instance.save()
        print('--------', direct_indicator_data)
        if len(direct_indicator_data):
            direct_indicator_data = direct_indicator_data[0]
            options = direct_indicator_data.pop('options')
            if instance.direct_indicator.exists():
                direct_indicator = instance.direct_indicator.all()[0]
            else:
                try:
                    di = DirectIndicator.objects.filter(method=instance.method, key=direct_indicator_data.get('key')).first()
                    di.delete()
                except DirectIndicator.DoesNotExist:
                    pass
                direct_indicator = DirectIndicator.objects.create(method=validated_data.get('method'), question=instance, key= direct_indicator_data.get('key'), name=direct_indicator_data.get('name'))
            direct_indicator.method = validated_data.get('method', direct_indicator.method)
            direct_indicator.key = direct_indicator_data.get('key', direct_indicator.key)
            direct_indicator.name = direct_indicator_data.get('name', direct_indicator.name)
            direct_indicator.description = direct_indicator_data.get('description', direct_indicator.description)
            direct_indicator.topic = validated_data.get('topic', direct_indicator.topic)
            direct_indicator.datatype = direct_indicator_data.get('datatype', direct_indicator.datatype)
            direct_indicator.pre_unit = direct_indicator_data.get('pre_unit', direct_indicator.pre_unit)
            direct_indicator.post_unit = direct_indicator_data.get('post_unit', direct_indicator.post_unit)

            direct_indicator.options.clear()
            for option in options:
                option_instance, _ = AnswerOption.objects.get_or_create(order=option.get('order', 1), text=option['text'])
                direct_indicator.options.add(option_instance.id)
            direct_indicator.save()
            
        return instance
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['section'] = instance.section.title

    #     return representation

    #TODO: Validation for possible UI Components.