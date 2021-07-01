from rest_framework import serializers

from ..models import Topic, Question

from .direct_indicator2 import DirectIndicatorSerializer2

# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['id', 'isMandatory', 'name', 'description', 'instruction', 'answertype']

class TopicSerializer(serializers.ModelSerializer):
    parent_topic_name = serializers.StringRelatedField(source='parent_topic', read_only=True)
    method = serializers.StringRelatedField()
    questions = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    direct_indicators = DirectIndicatorSerializer2(read_only=True, many=True)

    class Meta:
        model = Topic
        fields = ('id', 'parent_topic', 'name', 'description', 'parent_topic_name', 'method', 'questions', 'direct_indicators')
        read_only_fields = ['Method']
