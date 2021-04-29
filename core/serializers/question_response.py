from rest_framework import serializers

from ..models import QuestionResponse, QuestionOption


class QuestionResponseSerializer(serializers.ModelSerializer):
    values = serializers.SlugRelatedField(queryset=QuestionOption.objects.all(), many=True, slug_field='text')

    class Meta:
        model = QuestionResponse
        fields = ['id', 'direct_indicator_id', 'values', 'value']
        extra_kwargs = {'id': {'read_only': False, 'required': True}}