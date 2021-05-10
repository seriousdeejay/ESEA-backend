'''
from django.db import models

class CertificationLevel(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    level = models.IntegerField()
    method = models.ForeignKey('method', on_delete=models.CASCADE)


    def __str__(self):
        return self.name
'''