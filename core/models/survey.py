from django.db import models
from django.utils.translation import gettext_lazy as _

from .stakeholder_group import StakeholderGroup
# from .direct_indicator import DirectIndicator

def validate_max(value):
    if value > 100:
        raise ValidationError()

class SurveyManager(models.Manager):
    def create(self, name, method, description=None, stakeholdergroup=None, minThreshold=None, questions=None, anonymous=False):
        if stakeholdergroup:
            stakeholdergroup, _ = StakeholderGroup.objects.get_or_create(name=stakeholdergroup)
        survey = Survey(name=name, description=description, minThreshold=minTHreshold, anonymous=anonymous, method=method, stakeholdergroup=stakeholdergroup)
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
    method =  models.ForeignKey('Method', related_name="surveys", on_delete=models.CASCADE)
    # stakeholdergroup = models.OneToOneField('StakeholderGroup', related_name="response", on_delete=models.CASCADE)
    questions = models.ManyToManyField('DirectIndicator', related_name="surveys", blank=False) # Might be removable?

    name=models.CharField(max_length=255, unique=False, blank=False)
    description = models.CharField(max_length=1000, blank=True, null=True)
    welcome_text = models.CharField(max_length=1000, blank=True, null=True)
    closing_text = models.CharField(max_length=1000, blank=True, null=True)
    min_threshold = models.PositiveSmallIntegerField(null=True, default=100) # models.DecimalField(max_digits=5, decimal_places=2, default=0)
    anonymous = models.BooleanField(null=False, default=False)
    
    
    stakeholdergroup = models.ForeignKey('StakeholderGroup', related_name="surveys", on_delete=models.CASCADE) 
    # stakeholder_groups = models.ManyToManyField('StakeholderGroup')
    finished_responses = []

    MULTIPLE = "MULTIPLE"
    SINGLE = "SINGLE"

    RESPONSE_TYPES = (
        (MULTIPLE, "Multiple"),
        (SINGLE, "Single")
    )
    responseType = models.CharField(max_length=100, blank=False, choices=RESPONSE_TYPES, default="SINGLE")

    class Meta:
        verbose_name = _('survey')
        verbose_name_plural = _('surveys')

    def __str__(self):
        return self.name

    def finresponses(self):
        fresponses = [response for response in self.responses.all() if response.finished]
        self.finished_responses = fresponses
    
    def response_rate(self):
        responserate = (len(self.finished_responses)/(len(self.responses.all()) or 1)) * 100 #/
        return responserate


'''
- objects manager def create() should get parameter stakeholdergroup from yaml file
'''