from django.db import models

class CertificationLevel(models.Model):
    method = models.ForeignKey('Method', on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    level = models.IntegerField()
    # Hex color code
    colour = models.CharField(max_length=7)
    # requirements = models.ManyToManyField


    def __str__(self):
        return self.name
