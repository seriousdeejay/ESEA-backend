from django.db import models
from django.utils.translation import gettext_lazy as _

from .stakeholder_group import StakeholderGroup
# from .direct_indicator import DirectIndicator


class SurveyManager(models.Manager):
    def create(self, name, method, description=None, stakeholdergroup=None, rate=None, questions=None, anonymous=False):
        if stakeholdergroup:
            stakeholdergroup, _ = StakeholderGroup.objects.get_or_create(name=stakeholdergroup)
        survey = Survey(name=name, description=description, rate=rate, anonymous=anonymous, method=method, stakeholdergroup=stakeholdergroup)
        survey.save()
        # if stakeholdergroup:
        #     survey.stakeholder_groups.add(stakeholdergroup)
        survey.questions.set(questions)

        # directindicators = DirectIndicator.objects.filter(topic__method=method.id)
        # print('---', directindicators)
        # for di in directindicators: #.iterator()
        #     print(di)
        #     survey.questions.add(di)
        return survey

class Survey(models.Model):
    objects = SurveyManager()
    name=models.CharField(max_length=255, unique=False, blank=False)
    description = models.CharField(max_length=1000, blank=True, null=True)
    rate = models.PositiveSmallIntegerField(null=True, default=100) # models.DecimalField(max_digits=5, decimal_places=2, default=0)
    anonymous = models.BooleanField(null=False, default=False)
    questions = models.ManyToManyField('DirectIndicator', related_name="surveys", blank=False)
    method =  models.ForeignKey('Method', related_name="surveys", on_delete=models.CASCADE)
    stakeholdergroup = models.ForeignKey('StakeholderGroup', related_name="surveys", on_delete=models.CASCADE) 
    # stakeholder_groups = models.ManyToManyField('StakeholderGroup')
    finished_responses = []

    class Meta:
        verbose_name = _('survey')
        verbose_name_plural = _('surveys')

    def __str__(self):
        return self.name

    def finresponses(self):
        fresponses = [response for response in self.responses.all() if response.finished]
        self.finresponses = fresponses
    
    def response_rate(self):
        responserate = (len(self.finished_responses)/(len(self.responses.all()) or 1)) * 100 #/
        return responserate


'''
- objects manager def create() should get parameter stakeholdergroup from yaml file
'''