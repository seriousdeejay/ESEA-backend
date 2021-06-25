from django.db import models

class Section(models.Model):
    survey = models.ForeignKey('Survey', related_name='sections', on_delete=models.CASCADE, null=True)
    order = models.IntegerField(default=1)
    title = models.TextField(max_length=1000, blank=True)
    # questions = models.ManyToManyField('Question', related_name='section') #FK As well?


    def __str__(self):
        return self.title
