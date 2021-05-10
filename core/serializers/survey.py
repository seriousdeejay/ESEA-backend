from rest_framework import serializers

from ..models import Survey, StakeholderGroup, DirectIndicator, SurveyResponse
from .direct_indicator import DirectIndicatorSerializer


class SurveyOverviewSerializer(serializers.ModelSerializer):
    stakeholdergroup = serializers.SlugRelatedField(queryset=StakeholderGroup.objects.all(), slug_field="name")
    finished_responses = serializers.StringRelatedField(many=True, required=False)
    responses = serializers.PrimaryKeyRelatedField(queryset=SurveyResponse.objects.all() , many=True, required=False)
    questions = serializers.SlugRelatedField(queryset=DirectIndicator.objects.all(), many=True, slug_field='key')
    # stakeholdergroup = serializers.StringRelatedField(many=True, required=False)

 
    class Meta:
        model = Survey
        fields = ['id', 'name', 'description', 'min_threshold', 'anonymous', 'questions', 'method', 'stakeholdergroup', 'responses', 'finished_responses', 'response_rate'] #'stakeholdergroup'

    def validate_name(self, value):
        if self.instance and self.instance.name == value:
            return value

        survey = Survey.objects.filter(name=value)

        if survey.exists():
            raise serializers.ValidationError('Survey with this name exists already')

        return value

    def validate_minThreshold(self, value):
        if value > 100:
            raise serializers.ValidationError('Response rate should be a value between 0 and 100%')
        return value
    
    def validate_questions(self, value):
        if not len(value):
            raise serializers.ValidationError('A survey requires at least one question')
        return value

    def create(self, validated_data):
        return Survey.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
        # instance.stakeholder_groups.set(validated_data['stakeholders'])
        # if 'stakeholder_groups' in validated_data:
        #     validated_data['stakeholder_groups'] = self.update_stakeholders(
        #     stakeholder_groups=instance.stakeholder_groups, 
        #     name=validated_data['stakeholder_groups'], 
        #     method=instance.method)
        return super().update(instance, validated_data)
    
    def to_representation(self,instance):
        internal = {
           'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'min_threshold': instance.min_threshold,
            'anonymous': instance.anonymous,
            'questions': instance.questions,
            'method': instance.method,
            'stakeholdergroup': instance.stakeholdergroup,
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
    stakeholdergroup = serializers.CharField(read_only=True) #serializers.StringRelatedField(read_only=True, many=True)
    min_threshold = serializers.CharField(read_only=True)
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
                'stakeholdergroup': instance.stakeholdergroup,
                'min_threshold': instance.min_threshold,
                'topics': topic_list,
            }
        )