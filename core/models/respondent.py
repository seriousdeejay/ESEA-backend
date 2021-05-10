from django.db import models


class Respondent(models.Model):
    organisation = models.ForeignKey('Organisation', related_name="surveyrespondents", on_delete=models.CASCADE)

    
    email = models.EmailField(max_length=75, blank=False)
    first_name = models.CharField(max_length=50)
    last_name_prefix = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    # avatar = models.ImageField(blank=True, upload_to="respondent/", default="respondent/avatar-default.png")
    # esea_account = models.ForeignKey('ESeaAccount')

    def __str__(self):
        if self.last_name_prefix:
            return(f"{self.first_name} {self.last_name_prefix} {self.last_name}")
        return(f"{self.first_name} {self.last_name}")

'''
- Should be send a reminder if he hasn't filled in the survey a week before the campaign ends based on SurveyResponse.finished
'''