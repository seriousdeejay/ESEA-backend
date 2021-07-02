from django.db import models

class CertificationLevel(models.Model):
    method = models.ForeignKey('Method', on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    level = models.IntegerField()
    colour = models.CharField(max_length=7) # Hex color code
    # requirements = models.ManyToManyField


    def __str__(self):
        return self.name
