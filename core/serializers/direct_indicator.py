from typing import Union
from collections import OrderedDict
from rest_framework import serializers

from ..models import Question, DirectIndicator, Topic
from .question_option import QuestionOptionSerializer


class DirectIndicatorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    isMandatory = serializers.BooleanField()
    name = serializers.CharField(max_length=255, required=True)
    answertype = serializers.ChoiceField(required=True, choices=Question.QUESTION_TYPES)
    key = serializers.CharField(max_length=45, required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    pre_unit = serializers.CharField(required=False)
    post_unit = serializers.CharField(required=False)
    instruction = serializers.CharField(required=False, allow_blank=True)
    default = serializers.CharField(required=False, allow_blank=True)
    options = QuestionOptionSerializer(many=True)
    min_number = serializers.IntegerField(required=False)
    max_number = serializers.IntegerField(required=False)
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())

    def validate(self, data):
        type_with_options = Question.QUESTION_TYPES_WITH_OPTIONS

        if data["answertype"] in type_with_options and not len(data["options"]):
            raise serializers.ValidationError(
                f"{data['answertype']} requires options"
            )
        return data

    def validate_key(self, value):
        id = self.instance and self.instance.id
        topic_id = self.get_data("topic")
        key = self.get_data("key")

        direct_indicators = DirectIndicator.objects.filter(
            topic=topic_id, topic__method=self.initial_data["method"], key=key,
        ).exclude(pk=id)

        if len(direct_indicators):
            raise serializers.ValidationError("indicator key already used")

        return value

    def validate_name(self, value):
        id = self.instance and self.instance.id
        topic_id = self.get_data("topic")
        name = self.get_data("name")

        direct_indicators = DirectIndicator.objects.filter(
            topic=topic_id, question__name=name
        ).exclude(pk=id)

        if len(direct_indicators):
            raise serializers.ValidationError("duplicate question")

        return value

    def validate_topic(self, value):
        if value.method.pk != self.initial_data["method"]:
            raise serializers.ValidationError("Topic not found")

        return value

    def create(self, validated_data) -> DirectIndicator:
        return DirectIndicator.objects.create(**validated_data)

    def update(self, instance, validated_data) -> DirectIndicator:
        if len(instance.question.topics.all()) > 1:
            instance.delete()
            return self.create(validated_data)

        return instance.update(**validated_data)

    def to_representation(self, instance):
        """Convert instance to serializer attributes."""
        if isinstance(instance, DirectIndicator):
            internal = {
                "id": instance.id,
                "key": instance.key,
                "max_number": instance.question.max_number,
                "min_number": instance.question.min_number,
                "topic": instance.topic,
                "isMandatory": instance.question.isMandatory,
                "name": instance.question.name,
                "answertype": instance.question.answertype,
                "description": instance.question.description,
                "pre_unit": instance.pre_unit,
                "post_unit": instance.post_unit,
                "instruction": instance.question.instruction,
                "default": instance.question.default,
                "options": instance.question.options,
            }
        else:
            internal = instance

        result = super().to_representation(internal)
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] is not None]
        )

    def get_data(self, key) -> Union[str, int, bool]:
        if (
            key not in self.initial_data
            and self.instance
            and key in self.instance
        ):
            return self.instance[key]
        return self.initial_data[key]