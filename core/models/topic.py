from django.db import models
from django.utils.translation import gettext_lazy as _


class Topic(models.Model):
    name = models.CharField(max_length=120, unique=False, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    parent_topic = models.ForeignKey('Topic', related_name="sub_topics", blank=True, null=True, default=None, on_delete=models.CASCADE)
    method = models.ForeignKey('Method', related_name='topics', on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question', related_name="topics_of_questions", through='DirectIndicator')

    class Meta:
        verbose_name = _('topic')
        verbose_name_plural = _('topics')
    
    def __str__(self):
        return self.name
        