from rest_framework import serializers

from ..models import AnswerOption


class AnswerOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerOption
        fields = ['id', 'order', 'text']