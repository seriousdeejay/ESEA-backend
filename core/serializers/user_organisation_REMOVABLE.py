# from rest_framework import serializers

# from ..models import UserOrganisation
# from .survey_response import SurveyResponseSerializer

# class UserOrganisationSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.id')
#     organisation = serializers.ReadOnlyField(source='organisation.id')
#     user = serializers.StringRelatedField()
#     organisation = serializers.StringRelatedField()
#     stakeholdergroups = serializers.StringRelatedField(many=True)
#     survey_responses = serializers.StringRelatedField(many=True)

#     class Meta:
#         model = UserOrganisation
#         fields = ['id', 'user', 'organisation', 'role', 'stakeholdergroups', 'survey_responses']