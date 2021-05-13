from django.db import models
from django.utils.translation import gettext_lazy as _

from .stakeholder_group import StakeholderGroup

class SurveyManager(models.Manager):
    def create(self, name, method, questions, stakeholdergroup, description="", welcome_text="", closing_text="", min_threshold=100, response_type="SINGLE", anonymous=False):
        if stakeholdergroup:
            stakeholdergroup, _ = StakeholderGroup.objects.get_or_create(name=stakeholdergroup)
        survey = Survey(name=name, method=method, stakeholdergroup=stakeholdergroup, description=description, welcome_text=welcome_text, closing_text=closing_text, min_threshold=min_threshold, response_type=response_type, anonymous=anonymous,) # 
        survey.save()
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
    questions = models.ManyToManyField('DirectIndicator', related_name="surveys", blank=False) # Might be removable?
    stakeholdergroup = models.ForeignKey('StakeholderGroup', related_name="surveys", on_delete=models.CASCADE) 

    name=models.CharField(max_length=255, unique=False, blank=False)
    description = models.CharField(max_length=1000, blank=True)
    welcome_text = models.CharField(max_length=1000, blank=True)
    closing_text = models.CharField(max_length=1000, blank=True)
    min_threshold = models.PositiveSmallIntegerField(default=100)
    anonymous = models.BooleanField(null=False, default=False)
    
    finished_responses = []

    MULTIPLE = "MULTIPLE"
    SINGLE = "SINGLE"

    RESPONSE_TYPES = (
        (MULTIPLE, "Multiple"),
        (SINGLE, "Single")
    )
    response_type = models.CharField(max_length=100, choices=RESPONSE_TYPES, default="SINGLE")

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