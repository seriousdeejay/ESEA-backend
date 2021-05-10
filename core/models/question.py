from __future__ import annotations
from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _

from .question_option import QuestionOption


class questionManager(models.Manager):
    def create(self, isMandatory, name, topic, answertype, description=None, instruction=None, default=None, options=None):
        question = Question(isMandatory=isMandatory, name=name, topic=topic, answertype=answertype, description=description, instruction=instruction, default=default)
        question.save()

        if question.answertype in (question.QUESTION_TYPES_WITH_OPTIONS):
            print(question, answertype, options)
            for index, option in enumerate(options):
                questionoption = QuestionOption.objects.create(text=option, value=index + 1, question=question)
                question.options.add(questionoption)
            question.save()
        return question
    
    def get_or_create(self, **args):
        question = self.model.findQuestion(**args)
        if not question:
            question = self.model.objects.create(**args)
        return question

class Question(models.Model):
    topic = models.ForeignKey('Topic', related_name="questions_of_topic", on_delete=models.CASCADE)     # Needed, cause a many to many field can not be 'on_delete=models.CASCADE'
    topics = models.ManyToManyField("Topic", through="DirectIndicator")
    
    objects = questionManager()
    order = models.IntegerField(default=1)
    isMandatory = models.BooleanField(default=True) # Change to required
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True, null=True)
    instruction = models.TextField(blank=True, null=True)
    default = models.CharField(max_length=255, blank=True, default="")


    TEXT = "TEXT"
    NUMBER = "NUMBER"
    RADIO = "RADIO"
    CHECKBOX = "CHECKBOX"
    SCALE = "SCALE"
    # DROPDOWN = "DROPDOWN"
    QUESTION_TYPES = (
        (TEXT, "text"),
        (NUMBER, "number"),
        (RADIO, "radio"),
        (CHECKBOX, "checkbox"),
        (SCALE, "scale")
    )
    QUESTION_TYPES_WITH_OPTIONS = [RADIO, CHECKBOX, SCALE]
    answertype = models.CharField(max_length=100, blank=False, choices=QUESTION_TYPES, default="TEXT")

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return self.name

    def __repr__(self) -> str:  # -> str?
        return (
            f"<Question id='{self.id}' name='{self.name}' "
            f"answertype='{self.answertype}'>"
        )

    def hasOptions(self, options) -> bool:
        if not self.options.count() == len(options):
            return False

        optionsExists = True
        for inputOption in options:
            for option in self.options.all():
                if inputOption["text"] == option.text:
                    break
            if not option.equal(inputOption):
                optionsExists = False

        return optionsExists

    def findQuestion(name, answertype, options, description=None) -> Any: # instruction = None
        questions = Question.objects.filter(name=name, answertype=answertype, description=description)
        for question in questions:
            if question.hasOptions(options):
                return question
        return False

    def update(self, name, answertype, options, description=None, instruction=None, default=None) -> "Question":
        question: Question = Question.findQuestion(name, answertype, options, description)
        if question and question.id != self.id:
            self.delete()
            return question

        self.name = name
        self.answertype = answertype
        self.description = description
        self.instruction = instruction
        self.default = default
        self.save()

        if not self.hasOptions(options):
            self.options.all().delete()
            for option in options:
                QuestionOption.objects.create(question=self, **option)

        self.save()
        return self

 
    #options = models.ManyToManyField(QuestionOption, blank=True, related_name="ooo") 
    # options: QuestionOption

    ## TODO: Can i savely remove topic(s) fields from this model?