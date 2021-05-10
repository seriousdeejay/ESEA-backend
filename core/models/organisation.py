from django.db import models
from django.utils.translation import gettext_lazy as _


class Organisation(models.Model):
    created_by = models.ForeignKey('CustomUser', editable=False, on_delete=models.SET_NULL, null=True)
    esea_accounts = models.ManyToManyField('Method', through="EseaAccount", through_fields=('organisation', 'method'), related_name='organisations', blank=True)

    ispublic = models.BooleanField(default=True) # Change to is_public
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(blank=True, upload_to="organisation/", default="organisation/sustainability-circle.png")
   
    class Meta:
        verbose_name = _('organisation')
        verbose_name_plural = _('organisations')

    def __str__(self):
        return self.name

    # def relevant_survey_responses(self):
    #     return UserOrganisation.objects.filter(organisation=self, survey_responses__isnull=False).distinct()

    # members = models.ManyToManyField('CustomUser', through="UserOrganisation", through_fields=('organisation', 'user'), related_name='organisations', blank=True)

    '''
    - Should have image?
    - m2m method_organisations/ESEA_Account class to add a campaign class to?)
    '''