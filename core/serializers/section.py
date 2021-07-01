from rest_framework import serializers

from ..models import Section
from .text_fragment import TextFragmentSerializer
from .question import QuestionSerializer

class SectionSerializer(serializers.ModelSerializer):
    survey = serializers.StringRelatedField(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    text_fragments = TextFragmentSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'survey', 'order', 'title', 'questions', 'text_fragments']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['survey'] = instance.survey.name

        return representation

