from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from .survey import Survey
from .direct_indicator import DirectIndicator
from .question_response import QuestionResponse
import random
import string

class SurveyResponseManager(models.Manager):
    def create(self, survey, respondent, esea_account):
        token = "".join(random.choice(string.ascii_letters) for i in range(8))
        survey = get_object_or_404(Survey, id=survey)
        surveyresponse = SurveyResponse(survey=survey, respondent=respondent, esea_account=esea_account, token=token)
        surveyresponse.save()

        direct_indicators = DirectIndicator.objects.filter(surveys=survey)
        for direct_indicator in direct_indicators.values():
            question_response = QuestionResponse.objects.create(survey_response=surveyresponse, direct_indicator_id=direct_indicator['id'])
            question_response.save()

        return surveyresponse

class SurveyResponse(models.Model):
    objects = SurveyResponseManager()
    # id = models.BigIntegerField(primary_key = True)
    # id = models.AutoField(primary_key=True)
    esea_account = models.ForeignKey('EseaAccount', related_name="responses", on_delete=models.CASCADE, null=True)
    survey = models.ForeignKey('Survey', related_name="responses", on_delete=models.CASCADE)
    respondent = models.OneToOneField('Respondent', related_name="response", on_delete=models.CASCADE) # , primary_key=True, null=True for now!
    token = models.CharField(max_length=8)
    finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('survey_response')
        verbose_name_plural = _('survey_responses')
    
    def __str__(self):
        return f"'{self.survey} ({self.respondent})'"



    def filter_question_responses(self, question_responses):
        indicator_ids = self.survey.questions.values_list('id', flat=True,)
        return [
            question_response
            for question_response in question_responses
            if question_response['direct_indicator_id'] in indicator_ids
        ]

    def save_question_responses(self, question_responses):
        print('ssss', question_responses)
        filtered_question_responses = self.filter_question_responses(
            question_responses
        )
        question_response_mapping = {
            question_response.direct_indicator_id: question_response
            for question_response in self.question_responses.all()
        }
        data_mapping = {
            question_response['direct_indicator_id']: question_response
            for question_response in filtered_question_responses
        }
        print(question_response_mapping)
        print(data_mapping)

        # Perform creations and updates.
        question_response_list = []
        for id, data in data_mapping.items():
            print(data)
            question_response = question_response_mapping.get(id, None)
            if question_response is None:
                question_response_list.append(self.question_responses.create(**data))    
            else:
                pass
                # for value in data['values']:
                #     print(value)
                #     if value is not in (question_response.values):
                #          question_response.values.set(data['values'])
                #          question_response.save()
                # # question_response.values is not data['values']:
                # # question_response.values.set(data['values'])
                #         question_response_list.append(question_response)

        # Perform deletions.
        for id, question_response in question_response_mapping.items():
            if id not in data_mapping:
                question_response.delete()
        return question_response_list