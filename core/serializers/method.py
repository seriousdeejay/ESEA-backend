from rest_framework import serializers

from ..models import Method
from .survey import SurveyDetailSerializer
from .survey2 import SurveyDisplaySerializer
#from .topic import TopicSerializer
from .direct_indicator2 import DirectIndicatorSerializer2

class SubTopicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    parent_topic_name = serializers.StringRelatedField(source='parent_topic', read_only=True)
    questions = serializers.StringRelatedField(many=True)
    direct_indicators = DirectIndicatorSerializer2(read_only=True, many=True)

class TopicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    questions = serializers.StringRelatedField(many=True) #serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    direct_indicators = DirectIndicatorSerializer2(read_only=True, many=True)
    sub_topics = SubTopicSerializer(many=True)

class MethodSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    # surveys = SurveyDetailSerializer(read_only=True, many=True)
    # topics_names = serializers.StringRelatedField(source='topics',read_only=True, many=True)
    surveys = SurveyDisplaySerializer(read_only=True, many=True)
    #topics = serializers.StringRelatedField(read_only=True, many=True)
    topics = TopicSerializer(read_only=True, many=True)
    # organisations = serializers.StringRelatedField(read_only=True, many=True)
    networks = serializers.StringRelatedField(read_only=True, many=True)
    version = serializers.FloatField(required=False)

    class Meta:
        model = Method
        fields = ['id', 'created_by', 'ispublic', 'name', 'description', 'version', 'surveys', 'topics', 'networks']

    def validate_version(self, value):
        value = round(value, 2)
        return value

    def to_representation(self, instance):
        mytopics = {}

        for topic in instance.topics.all():
            if topic.parent_topic:
                parent = topic.parent_topic
                if parent.name not in mytopics.keys():
                    mytopics[parent.name] = {
                        'id': parent.id,
                        'name': parent.name,
                        'description': parent.description,
                        'questions': parent.questions,
                        'direct_indicators': parent.direct_indicators,
                        'sub_topics': [],
                    }
                mytopics[parent.name]['sub_topics'].append(
                    {
                        'id': topic.id,
                        'name': topic.name,
                        'description': topic.description,
                        'questions': topic.questions,
                        'direct_indicators': topic.direct_indicators,
                    })
        
        topic_list = []
        for _, topic in mytopics.items():
            topic_list.append(topic)
        
        # for _, sub_topics in sub_topics.items():

        representation = super().to_representation({
            'id': instance.id,
            'created_by': instance.created_by,
            'name': instance.name,
            'ispublic': instance.ispublic,
            'description': instance.description,
            'version': instance.version,
            'surveys': instance.surveys,
            'networks': instance.networks,
            'topics': topic_list
        })
        return representation



# class ResponsesSerializer(serializers.ModelSerializer):
#     user_organisation = UserOrganisationSerializer()
#     class Meta:
#         model = SurveyResponse
#         fields = '__all__'

# class SurveySerializer(serializers.ModelSerializer):
#     responses = ResponsesSerializer(many=True, read_only=True)
#     class Meta:
#         model = Survey
#         fields = ['id', 'name', 'description', 'rate', 'anonymous', 'questions', 'stakeholder_groups', 'responses']

    #surveyresponses = SurveyResponseSerializer(source='responses', read_only=True)
    # surveys = SurveySerializer(many=True, read_only=True)

    # networks = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
