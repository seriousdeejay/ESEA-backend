from rest_framework import serializers
from ..models import Method, Survey, Section, Question, DirectIndicator, StakeholderGroup

from .section import SectionSerializer

# class MethodField(serializers.RelatedField):
#     def to_representation(self, value):
#         print(value)
#         return value.name

#     def to_internal_value(self, value):
#         m = Method.objects.get(id=value)
#         return m

class SurveyDisplaySerializer(serializers.ModelSerializer):
    #method = MethodField(queryset=Method.objects.all())
    response_type = serializers.ChoiceField(choices=Survey.RESPONSE_TYPES)
    stakeholdergroup = serializers.SlugRelatedField(queryset=StakeholderGroup.objects.all(), slug_field="name")
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'method', 'name', 'description', 'response_type', 'min_threshold', 'anonymous', 'stakeholdergroup', 'welcome_text', 'closing_text', 'sections']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['method'] = instance.method.name

        return representation

    # def create(self, validated_data) -> Survey:
    #     return Survey.objects.create(**validated_data)

'''
    # name = serializers.CharField()
    # description = serializers.CharField(read_only=True)
    # min_threshold = serializers.IntegerField(read_only=True)
    # anonymous = serializers.BooleanField(read_only=True)
    # stakeholdergroup = serializers.CharField(read_only=True)
    # welcome_text = serializers.CharField(read_only=True)
    # closing_text = serializers.CharField(read_only=True)

class OptionsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.IntegerField(read_only=True)
    text = serializers.CharField(read_only=True)

class DirectIndicatorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    key = serializers.CharField(read_only=True)
    indicator_name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    topic = serializers.string_related_field(read_only=True)
    datatype = serializers.ChoiceField(read_only=True, choices=DirectIndicator.DATA_TYPES)
    pre_unit = serializers.CharField(read_only=True)
    post_unit = serializers.CharField(read_only=True)
    options = OptionsSerializer(many=True)





class CertificationLevelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    level = serializers.IntegerField(read_only=True)
    colour = serializers.CharField(read_only=True) # Should check for valid hexadecimal RGB string
    # requirements = indicators

class OptionsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.IntegerField(read_only=True)
    text = serializers.CharField(read_only=True)

class DirectIndicatorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    key = serializers.CharField(read_only=True)
    indicator_name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    topic = serializers.StringRelatedField(read_only=True)
    datatype = serializers.ChoiceField(read_only=True, choices=DirectIndicator.DATA_TYPES)
    pre_unit = serializers.CharField(read_only=True)
    post_unit = serializers.CharField(read_only=True)
    options = OptionsSerializer(many=True)

class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.IntegerField(read_only=True)
    is_mandatory = serializers.BooleanField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    instruction = serializers.CharField(read_only=True)
    uiComponent = serializers.ChoiceField(read_only=True, choices=Question.UI_COMPONENT_TYPES)
    direct_indicators = DirectIndicatorSerializer(many=True) 

class TextFragmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.IntegerField(read_only=True)
    text = serializers.CharField(read_only=True)


class SectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    questions = QuestionSerializer(many=True)
    text_fragments = TextFragmentSerializer(many=True)

    class Meta:
        model = Section
        fields = '__all__'
    #certification_levels = CertificationLevelSerializer(many=True)
'''



