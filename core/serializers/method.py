from rest_framework import serializers

from ..models import Method
from .survey import SurveyDetailSerializer

class MethodSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    surveys = SurveyDetailSerializer(read_only=True, many=True)
    organisations = serializers.StringRelatedField(read_only=True, many=True)
    networks = serializers.StringRelatedField(read_only=True, many=True)
    version = serializers.FloatField(required=False)

    class Meta:
        model = Method
        fields = ['id', 'ispublic', 'name', 'description', 'created_by', 'version', 'networks', 'organisations', 'surveys']

    def validate_version(self, value):
        value = round(value, 2)
        return value


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
