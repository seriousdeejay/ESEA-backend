from django.db import models


class Report(models.Model):
    esea_account = models.OneToOneField('EseaAccount', related_name="report", on_delete=models.CASCADE, primary_key=True)
    
    name = models.CharField(max_length=255, blank=False)
    # certification_grades = models.ManyToManyField('CertificationGrade', related_name="report", blank=True)

    def __str__(self):
        return self.name
