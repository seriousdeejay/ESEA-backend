from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from .models import EseaAccount, Respondent, SurveyResponse

@receiver(post_save, sender=EseaAccount)
def create_accountant_objects(sender, instance, created, **kwargs):
    respondent = Respondent.objects.create(organisation=instance.organisation, email="accountant@mail.com", first_name="Accountant", last_name=f"of {instance.organisation.name}")
    
    try:
        survey = instance.method.surveys.all().get(response_type="SINGLE")

    except ObjectDoesNotExist:
        print('No survey with responsetype "SINGLE" was found in the connected method.')
        instance.delete()
        respondent.delete()
        return
    
    surveyresponse = SurveyResponse.objects.create(survey=survey.id, esea_account=instance, respondent=respondent)
    
    

    