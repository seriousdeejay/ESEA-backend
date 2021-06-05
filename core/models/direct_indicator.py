from django.db import models
from django.utils.translation import gettext_lazy as  _

from .question import Question


class directIndicatorManager(models.Manager):
    def create(self, isMandatory, key, topic, name, answertype, survey=None,
        description="", pre_unit="", post_unit="", instruction="", default="", min_number=None, max_number=None, options=None):
        question = Question.objects.create(name=name, isMandatory=isMandatory, answertype=answertype, topic=topic, description=description, instruction=instruction, default=default, min_number=min_number, max_number=max_number, options=options)
        direct_indicator = DirectIndicator(key=key, question=question, topic=topic, pre_unit=pre_unit, post_unit=post_unit)
        direct_indicator.save()
        if survey:
            survey.questions.add(direct_indicator)

        return direct_indicator


class DirectIndicator(models.Model):
    objects = directIndicatorManager()
    question = models.ForeignKey("Question", related_name="direct_indicators", on_delete=models.CASCADE)
    topic = models.ForeignKey("Topic", related_name="direct_indicators", on_delete=models.CASCADE)

    key = models.CharField(max_length=45, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True, default="") 
    pre_unit = models.CharField(max_length=30, blank=True)      # Examples: $,€
    post_unit = models.CharField(max_length=30, blank=True)     # Examples: %, points, persons
    
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    DOUBLE = "DOUBLE"
    DATE = "DATE"
    BOOLEAN = "BOOLEAN"
    SINGLECHOICE = "SINGLECHOICE" # UI: RadioButton, Scale, Dropdown
    MULTIPLECHOICE = "MULTIPLECHOICE" # UI: Checkbox, Scale (1-3 on 1:10 scale for example)


    # QUESTION_TYPES = (
    #     (TEXT, "text"),
    #     (INTEGER, "integer"),
    #     (DOUBLE, "double"),
    #     (DATE, "date"),
    #     (BOOLEAN, "boolean"),
    #     (SINGLECHOICE, "singlechoice"),
    #     (MULTIPLECHOICE, "multiplechoice")
    # )

    # Datatype = models.CharField(max_length=50, blank=False, choices=QUESTION_TYPES, default="TEXT")

    responses = []
    value = None
    calculation_keys = None
    calculation = None

    class Meta:
        verbose_name = _("direct_indicator")
        verbose_name_plural = _("direct_indicators")

    @property
    def name(self):
        return self.question.name

    def __str__(self):
        return self.question.name

    def update(self, key, topic, name, answertype, isMandatory=True, options=None, description=None, instruction=None, default=None, min_number=None, max_number=None, pre_unit="", post_unit=""):
        self.key = key
        self.topic = topic
        self.pre_unit = pre_unit
        self.post_unit = post_unit
        self.question = self.question.update(name=name, answertype=answertype, isMandatory=isMandatory, options=options, description=description, instruction=instruction, default=default, min_number=min_number, max_number=max_number)
        self.save()
        return self

    def filter_responses(self, responses):
        self.responses = []
        # print(self.id)
        for response in responses:
            
            if response.direct_indicator_id == self.id:
                # print(response.values.all(), response.value)
                # print(response.direct_indicator_id, self.id)
                # print(self.question, self.question.answertype)
                if len(response.values.all()):
                    self.responses.append(response.values.all())
                else: 
                    self.responses.append(response.value)
        # self.responses = [
        #     response.values
        #     for response in responses
        #     if response.direct_indicator_id == self.id
        # ]
        self.value = self.get_average(self.responses)

    def get_average(self, responses=[]):
        response_values = responses
        if not len(responses):
            return "0"

        if (
            self.question.answertype == self.question.RADIO
            or self.question.answertype == self.question.CHECKBOX
            # or self.question.answertype == self.question.SCALE
        ):
            #print(self.question.answertype)
            response_values = self.checkbox_values(responses)
            return response_values


        return self.average_calculation(response_values)

    def average_calculation(self, responses):
        #print(responses)
        numbers = [int(r) for r in responses]
        return sum(numbers) / len(numbers)

    def checkbox_values(self, responses):
        valuesdict = {}
        for option in self.question.options.all():
            valuesdict[option.text] = 0
        #print(valuesdict['Fixed Salary'])
        #print(responses[0])
        #print('c')
        for response in responses:
            # options = response.split(",") # Splits it on commas, should be changed!!!
            # print('>>>', self.question, self.question.answertype)
            for option in response:
                # print(option)
                if option:
                    question_option = self.question.options.filter(text=option).first()
                    if question_option:
                        valuesdict[question_option.text] += 1
        return valuesdict

'''
- Should response_values not be returned to self.value (or self.values)?  [FIXED]
'''