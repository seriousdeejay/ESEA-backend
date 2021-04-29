import re
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from ..models import IndirectIndicator, DirectIndicator, Topic

find_questions_by_square_brackets = re.compile(r"\[.*?\]")

class IndirectIndicatorSerializer(WritableNestedModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())

    class Meta:
        model = IndirectIndicator
        fields = '__all__'

    def validate_topic(self, value):
        method_pk = self.initial_data['method']
        if value.method.pk != method_pk:
            raise serializers.ValidationError('Topic not found in method')
        return value

    def validate_formula(self, value):
        method_pk = self.initial_data['method']
        questions = re.findall(find_questions_by_square_brackets, value)
        if not len(questions):
            raise serializers.ValidationError("Needs to contain atleast one question")
        
        for question in questions:
            question = question[1:-1]
            try:
                DirectIndicator.objects.get(key=question, topic__method=method_pk)
            except Exception:
                raise serializers.ValidationError(f"Question with id '{question}' not found")
        
        return value
    
    def validate_name(self, value):
        method_pk = self.initial_data['method']

        if self.instance and self.instance.name == value:
            return value
        
        indirect_indicator = IndirectIndicator.objects.filter(name=value, topic__method=method_pk)

        if indirect_indicator.exists():
            raise serializers.ValidationError('Name is not unique')

        return value