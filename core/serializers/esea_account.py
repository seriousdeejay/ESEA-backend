from rest_framework import serializers

from ..models import EseaAccount, Organisation, Method, SurveyResponse

class MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Method
        fields = ['id', 'name', 'description']

class EseaAccountSerializer(serializers.ModelSerializer):
    organisation = serializers.SlugRelatedField(queryset=Organisation.objects.all(), slug_field='name')
    method = MethodSerializer(read_only=True)
    method = serializers.PrimaryKeyRelatedField(queryset=Method.objects.all())
    report = serializers.PrimaryKeyRelatedField(read_only=True)
    # response_rate = serializers.ReadOnlyField()
    all_responses = serializers.StringRelatedField(many=True, required=False)
    # responses = serializers.StringRelatedField(queryset=SurveyResponse.objects.filter(finished=True), many=True)
    
    class Meta:
        model = EseaAccount
        fields = ['id', 'organisation', 'method', 'campaign', 'network', 'report', 'all_respondents', 'all_responses', 'survey_response_by_survey', 'sufficient_responses', 'response_rate',]
        # extra_kwargs = {'survey_response_by_survey':{'many': True}}

    def update(self, instance, validated_data):
        print('chec1k')
        return instance