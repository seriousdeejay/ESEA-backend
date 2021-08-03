from rest_framework import serializers

from ..models import Survey, SurveyResponse, QuestionResponse, DirectIndicator
from .question_response import QuestionResponseSerializer

import random
import string


class SurveyResponseSerializer(serializers.ModelSerializer):
    question_responses = QuestionResponseSerializer(many=True, required=False)
    respondent = serializers.StringRelatedField()
    organisation = serializers.StringRelatedField(source='respondent.organisation')
    method = serializers.ReadOnlyField(source='survey.method.id')
    survey = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all(), required=True)
    class Meta:
        model = SurveyResponse
        fields = '__all__'
        read_only_fields = ['respondent', 'survey', 'organisation', 'method', 'token']

    def update(self, survey_response, validated_data):
        survey_response.finished = validated_data.get('finished', survey_response.finished)
        question_responses = validated_data.pop('question_responses')
        print(survey_response)
                        # question_responses_dict = dict((i.id, i) for i in survey_response.question_responses.all())
        for item_data in question_responses:
            qr, _ = QuestionResponse.objects.get_or_create(survey_response=survey_response, question=item_data.get('question'), direct_indicator_id=item_data.get('direct_indicator_id'))
            if 'values' in item_data.keys():
                if len(item_data['values']):
                    qr.values.clear()
                    for value in item_data['values']:
                        qr.values.add(value)
            qr.value = item_data.get('value', qr.value)
            qr.save()
            #         # question_response = QuestionResponse.objects.get(id=item_data['id']) #question_responses_dict.pop(item_data['id'])
            # for key in item_data.keys():
            #     if key == 'values':
            #         question_response.values.clear()
            #         for answer in item_data['values']:
            #             # print(QuestionOption.objects.filter(text='ddd').exists())
            #             try:
            #                 question_response.values.add(answer)
            #                 print('bb')
            #             except: 
            #                 print('cc')
            #     elif key == 'value':
            #         question_response.value = str(item_data['value'])
            #     else:
            #         setattr(question_response, key, item_data[key])
            # question_response.save()
        survey_response.save()
        return survey_response


class SurveyResponseCalculationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    topic = serializers.StringRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)
    key = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    formula = serializers.CharField(read_only=True)
    calculation = serializers.CharField(read_only=True)
    value = serializers.CharField(read_only=True)
    responses = serializers.ListField(child=serializers.CharField(read_only=True))


# class UserOrganisationField(serializers.RelatedField):
#     def to_representation(self, obj):
#         print('ddd', obj)
#         data = super(UserOrganisationSerializer).to_representation(obj)
#         return data

#     def to_internal_value(self, data):
#         try:
#             try:
#                 obj_id = data['id']
#                 return UserOrganisation.objects.get(id=obj_id)
#             except KeyError:
#                 raise serializers.ValidationError(
#                    'id is a required field.'
#                 )
#             except ValueError:
#                 raise serializers.ValidationError(
#                     'id must be an integer.'
#                 )
#         except UserOrganisation.DoesNotExist:
#             raise serializers.ValidationError(
#             'Obj does not exist.'
#             )
# class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
#     def __init__(self, **kwargs):
#         self.serializer = kwargs.pop('serializer', None)
#         if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
#             raise TypeError('"serializer" is not a valid serializer class')

#         super().__init__(**kwargs)

#     def use_pk_only_optimization(self):
#         return False if self.serializer else True

#     def to_representation(self, instance):
#         if self.serializer:
#             return self.serializer(instance, context=self.context).data
#         return super().to_representation(instance)

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['user_organisation'] = UserOrganisationSerializer(instance.user_organisation).data
    #     return response

    def create(self, validated_data):
        token = "".join(random.choice(string.ascii_letters) for i in range(8))
    #     user_organisation = validated_data.pop('respondent')
    #     print(validated_data)
    #     # print(user_organisation.survey_responses)
    #     direct_indicators = DirectIndicator.objects.filter(surveys=validated_data.get('survey'))
    #     survey_response = SurveyResponse.objects.create(**validated_data, token=token)

    #     for direct_indicator in direct_indicators.values():
    #         question_response = QuestionResponse.objects.create(survey_response=survey_response, direct_indicator_id=direct_indicator['id'])
    #         question_response.save()
    #     # survey_response.save_question_responses(question_responses)
    #     return survey_response

    #user_organisation = RelatedFieldAlternative(queryset=UserOrganisation.objects.all(), serializer=UserOrganisationSerializer)
    # surveyrespondent = SurveyRespondentSerializer(read_only=True)
    # user_organisation = UserOrganisationSerializer(read_only=True)

        # raise_errors_on_nested_writes('update', self, validated_data)
        # print(validated_data)
        # survey_response.question_responses.set = validated_data.get('question_responses', survey_response.question_responses)
        # for attr, value in validated_data.items():
        #     if attr == 'question_responses':
        #         for item in value:
        #             print('--->', item, item['direct_indicator_id'], item['values'])
        #             for answer in item['values']:
        #                 questionresponse, _ =  QuestionResponse.objects.get_or_create(id=item['id'])
        #                 print('||', questionresponse)
        #             # QuestionOption.objects.get(item['values'])
        #         # for attr, value in value.items():
        #         #     print(attr)
        #         # print('yeay!', value)
        #     # print('----', attr)
        #     else:
        #         setattr(survey_response, attr, value)
        #print(survey_response.question_responses.all())

    #     print(vars(survey_response))
    #     print('zzzzz', validated_data.get('question_responses', survey_response.question_responses))
    #     #question_responses = validated_data.get('question_responses', [])
    #    # survey_response.save_question_responses(question_responses)
    