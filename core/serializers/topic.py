from rest_framework import serializers

from ..models import Topic, Question, DirectIndicator, IndirectIndicator

from .direct_indicator2 import DirectIndicatorSerializer2
from .indirect_indicator import IndirectIndicatorSerializer

# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['id', 'isMandatory', 'name', 'description', 'instruction', 'answertype']

class TopicSerializer(serializers.ModelSerializer):
    parent_topic_name = serializers.StringRelatedField(source='parent_topic', read_only=True)
    method = serializers.StringRelatedField()
    questions = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    direct_indicators = serializers.ReadOnlyField()
    indirect_indicators = serializers.ReadOnlyField()
    # direct_indicators = serializers.PrimaryKeyRelatedField(queryset=DirectIndicator.objects.all(), many=True, required=False)
    # indirect_indicators = serializers.PrimaryKeyRelatedField(queryset=IndirectIndicator.objects.all(), many=True, required=False)

    class Meta:
        model = Topic
        fields = ('id', 'parent_topic', 'name', 'description', 'parent_topic_name', 'method', 'questions', 'direct_indicators', 'indirect_indicators')
        read_only_fields = ['Method']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        indicator_serializer = DirectIndicatorSerializer2(instance.direct_indicators, many=True)
        representation['direct_indicators'] = indicator_serializer.data

        indirect_indicator_serializer = IndirectIndicatorSerializer(instance.indirect_indicators, many=True)
        representation['indirect_indicators'] = indirect_indicator_serializer.data
        return representation