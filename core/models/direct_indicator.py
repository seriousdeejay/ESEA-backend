from django.db import models
from django.utils.translation import gettext_lazy as  _

from .question import Question
from .answer_option import AnswerOption

# question (FK) - Should be change to 1to1
# topic (FK)
# key
# name (= self.question.name)
# indicator_name
# (description)
# (pre_unit)
# (post_unit)
# datatype

class directIndicatorManager(models.Manager):
    def create(self, method,  key, name, datatype="Text", topic=None, description="", pre_unit="", post_unit="", question=None, answer_options=None, survey=None, wizard=False,
        answertype="TEXT", isMandatory=True, instruction="", default="", min_number=None, max_number=None, options=None):

        # If method creation wizard is used
        if wizard:
            question = Question.objects.create(name=name, isMandatory=isMandatory, answertype=answertype, topic=topic, description=description, instruction=instruction, default=default, min_number=min_number, max_number=max_number, options=options)

        direct_indicator = DirectIndicator(method=method, key=key, name=name, description=description, question=question, topic=topic, pre_unit=pre_unit, post_unit=post_unit, datatype=datatype)
        direct_indicator.save()

        if answer_options:
            for option in answer_options:
                print(option)
                answer_option, _ = AnswerOption.objects.get_or_create(order=option['Order'], text=option['Text'])
                direct_indicator.options.add(answer_option.id)
                #direct_indicator.options.add(answer_option)
    
        direct_indicator.save()

        print(direct_indicator.options)

        if survey:
            survey.questions.add(direct_indicator)

        return direct_indicator


class DirectIndicator(models.Model):
    objects = directIndicatorManager()
    question = models.ForeignKey("Question", related_name="direct_indicator", on_delete=models.CASCADE, null=True)
    # One to One field? question2 = models.OneToOneField("Question", on_delete=models.CASCADE, null=True, primary_key=False)
    method = models.ForeignKey("Method", related_name="direct_indicators", on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey("Topic", related_name="direct_indicators", on_delete=models.CASCADE, null=True)

    key = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True, default="") 
    pre_unit = models.CharField(max_length=30, blank=True, default="")      # Examples: $,€
    post_unit = models.CharField(max_length=30, blank=True, default="")     # Examples: %, points, persons
    #min number
    #max number

    TEXT = "text"
    INTEGER = "integer"
    DOUBLE = "double"
    DATE = "date"
    BOOLEAN = "boolean"
    SINGLECHOICE = "singlechoice" # UI: RadioButton, Scale, Dropdown
    MULTIPLECHOICE = "multipleChoice" # UI: Checkbox, Scale (1-3 on 1:10 scale for example)

    DATA_TYPES = (
        (TEXT, "text"),
        (INTEGER, "Integer"),
        (DOUBLE, "double"),
        (DATE, "date"),
        (BOOLEAN, "boolean"),
        (SINGLECHOICE, "singlechoice"),
        (MULTIPLECHOICE, "multiplechoice")
    )

    datatype = models.CharField(max_length=50, blank=False, choices=DATA_TYPES, default="text")

    responses = []
    value = None
    calculation_keys = None
    calculation = None

    class Meta:
        verbose_name = _("direct_indicator")
        verbose_name_plural = _("direct_indicators")

    @property
    def question_name(self):
        if self.question:
            return self.question.name
        return ''

    def __str__(self):
        return self.name

    def update(self, key, name, answertype, topic=None, isMandatory=True, options=None, description=None, instruction=None, default=None, min_number=None, max_number=None, pre_unit="", post_unit=""): # Add datatype?
        print('-->', topic)
        self.key = key
        self.topic = topic
        self.pre_unit = pre_unit
        self.post_unit = post_unit
        self.question = self.question.update(name=name, answertype=answertype, isMandatory=isMandatory, options=options, description=description, instruction=instruction, default=default, min_number=min_number, max_number=max_number)

        # if not self.hasOptions(options):
        #     self.options.all().delete()
        #     for option in options:
        #         QuestionOption.objects.create(question=self, **option)

        self.save()
        return self

    def filter_responses(self, responses):
        self.responses = []

        for response in responses:
            if response.direct_indicator_id == self.id:
                if len(response.values.all()):
                    self.responses.append(response.values.all())
                else: 
                    self.responses.append(response.value)

        self.value = self.get_average(self.responses)

    def get_average(self, responses=[]):
        response_values = responses
        if not len(responses):
            return "0"

        if (
            self.datatype == self.SINGLECHOICE
            or self.datatype == self.BOOLEAN
            or self.datatype == self.MULTIPLECHOICE
        ):
            response_values = self.checkbox_values(responses)
            return response_values

        return self.average_calculation(response_values)

    def average_calculation(self, responses):
        numbers = [int(r) for r in responses]
        return sum(numbers) / len(numbers)

    def checkbox_values(self, responses):
        valuesdict = {}

        for option in self.options.all():
            valuesdict[option.text] = 0
        for response in responses:
            if response:
                question_option = self.options.filter(text=response).first()
                if question_option:
                    valuesdict[question_option.text] += 1
        if (self.datatype == self.SINGLECHOICE or self.datatype == self.BOOLEAN):
            if self.question.section.survey.response_type == 'single':
                return max(valuesdict, key=valuesdict.get) if valuesdict else None
        return valuesdict



'''
- Should response_values not be returned to self.value (or self.values)?  [FIXED]
'''



            # options = response.split(",") # Splits it on commas, should be changed!!!
            # print('>>>', self.question, self.question.answertype)


        # print('responses":', responses)
        # self.responses = [
        #     response.values
        #     for response in responses
        #     if response.direct_indicator_id == self.id
        # ]
                        # print(response.values.all(), response.value)
                # print(response.direct_indicator_id, self.id)
                # print(self.question, self.question.answertype)