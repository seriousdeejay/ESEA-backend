from rest_framework import serializers
from ..models import Survey, Question, DirectIndicator

'''
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

class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.IntegerField(read_only=True)
    is_mandatory = serializers.BooleanField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    instruction = serializers.CharField(read_only=True)
    uiComponent = serializers.ChoiceField(read_only=True, choices=Question.UI_COMPONENT_TYPES)
    direct_indicator = DirectIndicatorSerializer() 

class TextFragment(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.IntegerField(read_only=True)
    text = serializers.CharField(read_only=True)

class CertificationLevelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    level = serializers.IntegerField(read_only=True)
    colour = serializers.CharField(read_only=True) # Should check for valid hexadecimal RGB string
    # requirements = indicators


class SectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    questions = QuestionSerializer(many=True)
    text_fragments = TextFragmentSerializer(many=True)
    certification_levels = CertificationLevelSerializer(many=True)
'''

class SurveyDisplaySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    response_type = serializers.ChoiceField(read_only=True, choices=Survey.RESPONSE_TYPES)
    min_threshold = serializers.IntegerField(read_only=True)
    anonymous = serializers.BooleanField(read_only=True)
    stakeholdergroup = serializers.CharField(read_only=True)
    welcome_text = serializers.CharField(read_only=True)
    closing_text = serializers.CharField(read_only=True)
    #sections = SectionSerializer(many=True)

    #questions = serializers.StringRelatedField(read_only=True, many=True)
    #questions = DirectIndicatorSerializer(many=True)
    #topics = SurveyTopicSerializer(many=True)




