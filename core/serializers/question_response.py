from rest_framework import serializers

from ..models import QuestionResponse, AnswerOption, DirectIndicator


class QuestionResponseSerializer(serializers.ModelSerializer):
    values = serializers.SlugRelatedField(queryset=AnswerOption.objects.all(), many=True, slug_field='text')

    class Meta:
        model = QuestionResponse
        fields = ['id', 'question', 'direct_indicator_id', 'values', 'value']

    def validate(self, data):
        value = data['value']
        if value:
            if data["direct_indicator_id"] > 0: 
                Di = DirectIndicator.objects.get(id=data["direct_indicator_id"])

                if Di.datatype == 'integer':
                    try:
                        int(value)
                    except:
                        raise serializers.ValidationError('Question response should be of type integer')

                if Di.datatype == 'double':
                    try:
                        float(value)
                    except:
                        raise serializers.ValidationError('Question response should be of type double')

                if Di.datatype == 'date':
                    print('is it a date?')
                    # try:
                    # except:

                if Di.datatype in ['boolean', 'singlechoice']:
                    print('Is only one value returned?')
                    # try:
                    # except:

                if Di.datatype == 'multiplechoice':
                    print('is a list of QuestionOptions returned?')
                    # try:
                    # except:

        return data




 # extra_kwargs = {'id': {'read_only': False, 'required': True}}