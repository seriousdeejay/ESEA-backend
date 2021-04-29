'''
from django.db import models

class CertificationGrade(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    grade = models.IntegerField()

    def __str__(self):
        return self.name
'''