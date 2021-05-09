from rest_framework import serializers

from ..models import Campaign, EseaAccount, Method, Network, Respondent, SurveyResponse, Survey
from .esea_account import EseaAccountSerializer
from datetime import datetime
import pytz

class CampaignSerializer(serializers.ModelSerializer):
    organisation_accounts = EseaAccountSerializer(many=True, read_only=True)
    network = serializers.PrimaryKeyRelatedField(queryset=Network.objects.all())
    method = serializers.PrimaryKeyRelatedField(queryset=Method.objects.all())
    # open_survey_date = serializers.DateTimeField()
    # method = serializers.SlugRelatedField(queryset=Method.objects.all(), slug_field='name')

    # method = serializers.StringRelatedField()
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'image', 'network', 'method', 'organisation_accounts', 'open_survey_date', 'close_survey_date']
        depth = 1

    def validate_open_survey_date(self, value):
        
        if datetime.now(pytz.utc) > value:
            raise serializers.ValidationError('Opening date should be in the future.')
        return value

    def validate_close_survey_date(self, value):
        print('my time:', value)
        try:
            start_date = datetime.strptime(self.initial_data['open_survey_date'], '%Y-%m-%dT%H:%M:%S%z') #.%f
        except:
            start_date = datetime.strptime(self.initial_data['open_survey_date'], '%Y-%m-%dT%H:%M:%S.%f%z')
        
        if start_date > value:
            raise serializers.ValidationError('Closing date must be after Opening date.')
        return value
    
    def create(self, validated_data):
        campaign = Campaign.objects.create(**validated_data)
        for organisation in campaign.network.organisations.all():
            eseaaccount = EseaAccount.objects.create(organisation=organisation, method=campaign.method, campaign=campaign)
            r = Respondent.objects.create(organisation=organisation, email="accountant@localhost.com", first_name="accountant", last_name_prefix="of", last_name=organisation.name)
            accountant_survey = Survey.objects.filter(method=campaign.method, stakeholdergroup__name="accountant").first()
            SurveyResponse.objects.create(survey=accountant_survey.id, respondent=r, esea_account=eseaaccount)
        return campaign


    # def to_representation(self, instance):
    #     data = super(CampaignSerializer, self).to_representation(instance)
    #     data['method'] = serializers.StringRelatedField()
    #     return data