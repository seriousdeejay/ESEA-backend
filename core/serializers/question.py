from rest_framework import serializers

from ..models import Question, DirectIndicator
from .answer_option import AnswerOptionSerializer
from .direct_indicator2 import DirectIndicatorSerializer2


class QuestionSerializer(serializers.ModelSerializer):
    uiComponent = serializers.ChoiceField(choices=Question.UI_COMPONENT_TYPES)
    direct_indicator = DirectIndicatorSerializer2(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
        'id', 
        'section',  
        'order', 
        'isMandatory', 
        'name', # R
        'description', 
        'instruction', 
        'uiComponent',  # R
        'direct_indicator'
        ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['section'] = instance.section.title

        return representation

    #TODO: Validation for possible UI Components.