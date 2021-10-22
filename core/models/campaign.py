from django.db import models
from django.utils.timezone import now
from datetime import timedelta, date


def defaultrespondingwindow():
        return now() + timedelta(days = 30)

class Campaign(models.Model):
    created_by = models.ForeignKey('CustomUser', editable=False, on_delete=models.SET_NULL, null=True)
    network = models.ForeignKey('Network', related_name="campaigns", on_delete=models.CASCADE)
    method = models.ForeignKey('method', on_delete=models.CASCADE) # If a method gets removed the network_method gets removed too, is this a good choice?

    required = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to="campaign/", default="campaign/campaign-default.png")
    year = models.IntegerField(default=date.today().year)
    open_survey_date = models.DateTimeField(default=now)
    close_survey_date = models.DateTimeField(default=defaultrespondingwindow)
    close_validation_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} (method: {self.method})'

    def save(self, *args, **kwargs):
        if self.close_validation_date is None and self.close_survey_date is not None:
            self.close_validation_date = self.close_survey_date + timedelta(days = 14)
        super(Campaign, self).save(*args, **kwargs)




''' 
- Should have name field
- Could have created_on = models.DateTimeField(default=now, editable=False)
- Should return self.name in __str__ method
'''