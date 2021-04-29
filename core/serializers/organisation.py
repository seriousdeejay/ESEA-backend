from rest_framework import serializers
from ..models import Organisation, SurveyResponse


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['id', 'finished', 'survey']


class OrganisationSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    # organisation_members = UserOrganisationSerializer(many=True, required=False, source="relevant_survey_responses", read_only=True)

    class Meta:
        model = Organisation
        fields = ['id', 'ispublic', 'name', 'description', 'image', 'created_by', 'networks', 'esea_accounts']
        extra_kwargs = {'networks': {'required': False}, 'methods': {'required': False}}


# from rest_framework.fields import CurrentUserDefault
# class OrganisationSerializer(serializers.ModelSerializer):
#     # organisation_members = UserOrganisationSerializer(many=True, required=False)
#     created_by = serializers.StringRelatedField()
#     organisation_members = UserOrganisationSerializer(many=True, required=False)
#     class Meta:
#         model = Organisation        
#         fields = ['id', 'ispublic', 'name', 'description', 'created_by', 'organisation_members']


# class FilteredListSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         data = data.filter(user=self.context['request'].user, edition__hide=False)
#         return super(FilteredListSerializer, self).to_representation(data)


# class UserOrganisationSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()
#     stakeholdergroups = serializers.StringRelatedField(many=True)
#     survey_responses = SurveyResponseSerializer(many=True, required=False, read_only=True)

#     class Meta:
#         model = UserOrganisation
#         fields = ['id', 'user', 'organisation', 'stakeholdergroups', 'survey_responses']