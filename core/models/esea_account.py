from django.db import models
from django.shortcuts import get_object_or_404
from .respondent import Respondent
from .survey_response import SurveyResponse
from datetime import date


class EseaAccount(models.Model):
    method = models.ForeignKey("Method", on_delete=models.CASCADE)
    organisation = models.ForeignKey("Organisation", related_name="esea_accounts", on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', related_name="organisation_accounts", on_delete=models.CASCADE, null=True)

    year = models.IntegerField(default=date.today().year)
    sufficient_responses = models.BooleanField(default=False)      # Same as Status: Enum for now
    response_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    '''
    SUFFICIENT = "SUFFICIENT"
    UNSUFFICIENT = "UNSUFFICIENT"

    STATUS_OPTIONS = (
        (SUFFICIENT, "Sufficient"),  # or Complete
        (UNSUFFICIENT, "Unsufficient"), # or Incomplete
        (ONGOING, 'Ongoing'),
        # Add in more status options
    )
    status = models.CharField(max_length=100, blank=False, choices=STATUS_OPTIONS, default="UNSUFFICIENT")
    '''

    def __str__(self):
        return f'organisation:{self.organisation} - campaign:{self.campaign}'
    
    @property           # Should i keep this network property?
    def network(self):
        return self.campaign.network

    def survey_response_by_survey(self):
        arr = []
        for survey in self.method.surveys.all():
            tempdict = {'id': survey.id, 'name': survey.name, 'questions': [], 'stakeholdergroup': str(survey.stakeholdergroup), 'type': survey.response_type} # 'questions': len(survey.questions.all())
            tempdict['respondees'] = [{'name':str(respondee)} for respondee in Respondent.objects.filter(response__esea_account=self, response__survey=survey).distinct()]
            tempdict['responses'] = len(self.responses.filter(survey=survey, finished=True))
            tempdict['required_response_rate'] = survey.min_threshold
            tempdict['current_response_rate'] = int((tempdict['responses'])/(len((tempdict['respondees'])) or 1))
            tempdict['sufficient_responses'] = tempdict['current_response_rate'] >= tempdict['required_response_rate']
            arr.append(tempdict)
        responserates = [item['current_response_rate'] for item in arr]
        self.response_rate = (sum(responserates)/len(responserates))
        
        for survey in arr:
            if (survey['sufficient_responses'] == False):
                return arr
        self.sufficient_responses = True
        return arr

    def all_respondents(self):
        respondents = len(Respondent.objects.filter(response__esea_account=self))            
        return respondents

    def all_responses(self):
        responses = SurveyResponse.objects.filter(esea_account=self, finished=True)
        return responses










'''
    @property
    def response_rate(self):
        response_rate_dict = {}
        overall_finished_responses = 0
        for survey in self.method.surveys.all():
            finished_responses = [response for response in self.responses.all() if (response.finished == True & response.survey == survey)]
            overall_finished_responses += len(finished_responses)
            sum = (len(finished_responses)/(len(self.responses.all()) or 1) * 100) 
            sum = round(sum,2)
            response_rate_dict[survey.name] = {'rate': sum, 'required': survey.rate}
        self.all_response_rate(overall_finished_responses)
        return response_rate_dict

    def sufficient_response_rate(self):
        Bool = True
        for survey in self.response_rate:
            innerdict = self.response_rate[survey]
            if (innerdict['rate'] >= innerdict['required']):
                print(f'The response rate of {survey} is high enough!')
            else:
                print(f'The response rate of {survey} is not high enough!')
                Bool = False

        self.sufficient_responses = Bool
    
    def all_response_rate(self, finished_responses):
        self.all_response_rate = (finished_responses/(len(self.responses.all()) or 1)) * 100
'''

''' 
- Should change __str__ return
'''