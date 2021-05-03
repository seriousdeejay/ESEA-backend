from rest_framework import serializers

from ..models import Survey, StakeholderGroup, DirectIndicator, SurveyResponse
from .direct_indicator import DirectIndicatorSerializer


class SurveyOverviewSerializer(serializers.ModelSerializer):
    stakeholders = serializers.StringRelatedField(many=True, required=False)
    finished_responses = serializers.StringRelatedField(many=True, required=False)
    responses = serializers.PrimaryKeyRelatedField(queryset=SurveyResponse.objects.all() , many=True, required=False)
    questions = serializers.SlugRelatedField(queryset=DirectIndicator.objects.all(), many=True, slug_field='key')
    stakeholdergroup = serializers.StringRelatedField()

 
    class Meta:
        model = Survey
        fields = ['id', 'name', 'description', 'rate', 'anonymous', 'questions', 'method', 'stakeholders', 'stakeholdergroup', 'responses', 'finished_responses', 'response_rate']

    def create(self, validated_data):
        return Survey.objects.create(**validated_data)

    def update(self, instance, validated_data): 
        if 'stakeholder_groups' in validated_data:
            validated_data['stakeholder_groups'] = self.update_stakeholders(
            stakeholder_groups=instance.stakeholder_groups, 
            name=validated_data['stakeholder_groups'], 
            method=instance.method)
        return super().update(instance, validated_data)
    
    def to_representation(self,instance):
        internal = {
           'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'rate': instance.rate,
            'anonymous': instance.anonymous,
            'questions': instance.questions,
            'method': instance.method,
            'stakeholders': instance.stakeholder_groups,
            'responses': instance.responses,
            'finished_responses': instance.finished_responses,
            'response_rate': instance.response_rate
        }
        return super().to_representation(internal)

    # def update_stakeholder(self, stakeholder_groups, name, method):
    #     if len(stakeholder_group.surveys.all()) > 1:
    #         stakeholder, _ = StakeholderGroup.objects.get_or_create(name=name, method=method)
    #         return stakeholder
    #     return stakeholder_group.update(name=name)

    
class SurveyQuestionOptionSerializer(serializers.Serializer):
    text = serializers.CharField(read_only=True)
    value = serializers.CharField(read_only=True)


class SurveySubTopicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    questions = DirectIndicatorSerializer(many=True)


class SurveyTopicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    questions = DirectIndicatorSerializer(many=True)
    sub_topics = SurveySubTopicSerializer(many=True)


class SurveyDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    method = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    stakeholders = serializers.StringRelatedField(read_only=True, many=True)
    rate = serializers.CharField(read_only=True)
    topics = SurveyTopicSerializer(many=True)

    def to_representation(self, instance):
        direct_indicators = instance.questions.all()
        topics = {}
        sub_topics = {}

        for direct_indicator in direct_indicators:
            topic_list = topics
            topic = direct_indicator.topic

            if topic.parent_topic:
                topic_list = sub_topics

            if topic.name not in topic_list.keys():
                topic_list[topic.name] = {
                    'id': topic.id,
                    'name': topic.name,
                    'description': topic.description,
                    'parent_topic': topic.parent_topic,
                    'questions': [direct_indicator],
                    'sub_topics': [],
                }
            else:
                topic_list[topic.name]['questions'].append(direct_indicator)

        for _, sub_topic in sub_topics.items():
            parent = sub_topic['parent_topic']
            if parent.name not in topics:
                topics[parent.name] = {
                    'id': parent.id,
                    'name': parent.name,
                    'description': parent.description,
                    'questions': [],
                    'sub_topics': [],
                }

            sub_topic['parent_topic'] = sub_topic['parent_topic'].name
            parent = sub_topic['parent_topic']
            if 'sub_topics' in topics[parent]:
                topics[parent]['sub_topics'].append(sub_topic)
            else:
                topics[parent] = {
                    **topics[parent],
                    'sub_topics': [sub_topic],
                }

        topic_list = []
        for _, topic in topics.items():
            topic_list.append(topic)

        return super().to_representation(
            {
                'id': instance.id,
                'name': instance.name,
                'description': instance.description,
                'method': instance.method,
                'stakeholders': instance.stakeholder_groups,
                'rate': instance.rate,
                'topics': topic_list,
            }
        )