from rest_framework import serializers

from ..models import Topic, Question


# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['id', 'isMandatory', 'name', 'description', 'instruction', 'answertype']

class TopicSerializer(serializers.ModelSerializer):
    parent_topic_name = serializers.StringRelatedField(source='parent_topic', read_only=True)
    method = serializers.StringRelatedField()
    questions = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Topic
        fields = ('id', 'parent_topic', 'name', 'description', 'parent_topic_name', 'method', 'questions')
        read_only_fields = ['Method']