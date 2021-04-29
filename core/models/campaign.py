from django.db import models
from django.utils.timezone import now
from datetime import timedelta

def defaultrespondingwindow():
        return now() + timedelta(days = 30)

class Campaign(models.Model):
    name = models.CharField(max_length=255, default="A New Campaign")
    network = models.ForeignKey('Network', on_delete=models.CASCADE)
    method = models.ForeignKey('method', on_delete=models.CASCADE) # If a method gets removed the network_method gets removed too, is this a good choice?
    image = models.ImageField(blank=True, upload_to="campaign/", default="campaign/campaign-default.png")
    created_by = models.ForeignKey('CustomUser', editable=False, on_delete=models.SET_NULL, null=True)
    # created_on = models.DateTimeField(default=now, editable=False)
    required = models.BooleanField(default=True)
    open_survey_date = models.DateTimeField(default=now)
    close_survey_date = models.DateTimeField(default=defaultrespondingwindow)
    # close_validation_date = models.DateTimeField()

    def __str__(self):
        return f'{self.name} (method: {self.method})'

''' 
- Should have name field
- Should return self.name in __str__
'''