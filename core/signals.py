from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from .models import EseaAccount, Respondent, Survey, SurveyResponse, Campaign

@receiver(post_save, sender=EseaAccount)
def create_accountant_objects(sender, instance, created, **kwargs):
    respondent = Respondent.objects.create(organisation=instance.organisation, email="accountant@mail.com", first_name="Accountant", last_name=f"of {instance.organisation.name}")
    print(respondent)
    try:
        survey = instance.method.surveys.all().get(response_type="SINGLE")
        print(survey)
    except ObjectDoesNotExist:
        print('No survey with responsetype "SINGLE" was found in the connected method.')
        instance.delete()
        respondent.delete()
        return
    
    surveyresponse = SurveyResponse.objects.create(survey=survey.id, esea_account=instance, respondent=respondent)
    print(surveyresponse)
    
@receiver(post_save, sender=Campaign)
def create_esea_accounts(sender, instance, created, **kwargs):
    print(instance.method.surveys.all().filter(response_type="SINGLE"))
    for organisation in instance.network.organisations.all():
        eseaaccount = EseaAccount.objects.get_or_create(organisation=organisation, method=instance.method, campaign=instance)
        print("my eseaaccount")
    print('campaign saved', instance.organisation_accounts)


    