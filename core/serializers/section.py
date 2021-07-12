from rest_framework import serializers

from ..models import Section, Question
from .text_fragment import TextFragmentSerializer
from .question import QuestionSerializer

class SectionSerializer(serializers.ModelSerializer):
    # survey = serializers.StringRelatedField(read_only=True)
    #questions =  QuestionSerializer(many=True, read_only=True)
    questions = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), many=True)
    text_fragments = TextFragmentSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'survey', 'order', 'title', 'questions', 'text_fragments']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(instance.questions.all())
        question_serializer = QuestionSerializer(instance.questions, many=True)
        print(question_serializer.data)
        representation['questions'] = question_serializer.data
        return representation
