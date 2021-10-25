from rest_framework import serializers

from ..models import EseaAccount, Organisation, Method, Network, Campaign, SurveyResponse, Respondent


class MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Method
        fields = ['id', 'name', 'description']

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ['id', 'name']

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name']

class EseaAccountSerializer(serializers.ModelSerializer):
    # organisation = serializers.SlugRelatedField(queryset=Organisation.objects.all(), slug_field='name')
    organisation_name = serializers.ReadOnlyField(source='organisation.name')
    method_name = serializers.ReadOnlyField(source='method.name')
    campaign_name = serializers.ReadOnlyField(source='campaign.name')
    # method = MethodSerializer(read_only=True)
    # method = serializers.PrimaryKeyRelatedField(queryset=Method.objects.all(), write_only=True)
    report = serializers.PrimaryKeyRelatedField(read_only=True)
    all_responses = serializers.StringRelatedField(many=True, required=False)
    
    class Meta:
        model = EseaAccount
        fields = ['id', 'year', 'organisation', 'organisation_name', 'method', 'method_name', 'campaign', 'campaign_name', 'report', 'all_respondents', 'all_responses', 'survey_response_by_survey', 'deployed_to_respondents', 'sufficient_responses', 'response_rate']

    def create(self, validated_data):
        return EseaAccount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.campaign:
            representation['network'] = instance.campaign.network.id
            representation['network_name'] = instance.campaign.network.name

        return representation




    # responses = serializers.StringRelatedField(queryset=SurveyResponse.objects.filter(finished=True), many=True)