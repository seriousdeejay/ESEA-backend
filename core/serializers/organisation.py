from rest_framework import serializers
from ..models import Organisation, OrganisationMember, Network


class OrganisationSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    created_by_id = serializers.ReadOnlyField(source='created_by.id')
    image = serializers.ImageField(required=False)
    esea_accounts = serializers.StringRelatedField(read_only=True, many=True)
    networks = serializers.PrimaryKeyRelatedField(queryset=Network.objects.all(), many=True, required=False)

    class Meta:
        model = Organisation
        fields = ['id', 'ispublic', 'name', 'description', 'image', 'created_by', 'created_by_id', 'networks', 'esea_accounts']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user=self.context['request'].user

        if user.is_superuser:
            representation['accesLevel'] = "admin"
        else:
            try:
                member = OrganisationMember.objects.get(organisation=instance, user=user)
            except OrganisationMember.DoesNotExist:
                member = None
            
            if member:
                representation['accesLevel'] = member.get_role_display()
        return representation

    def create(self, validated_data):
        user=self.context['request'].user
        
        organisation = Organisation.objects.create(**validated_data)
        OrganisationMember.objects.create(organisation=organisation, user=user, role=3, invitation='accepted')

        return organisation

# class SurveyResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SurveyResponse
#         fields = ['id', 'finished', 'survey']


# organisation_members = UserOrganisationSerializer(many=True, required=False, source="relevant_survey_responses", read_only=True)
#, 'methods': {'required': False}}


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