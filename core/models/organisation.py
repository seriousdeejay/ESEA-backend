from django.db import models
from django.utils.translation import gettext_lazy as _

from .organisation_member import OrganisationMember


class OrganisationManager(models.Manager):
    def create(self, name, created_by, ispublic=True, description=""):
        
        organisation_instance = Organisation(name=name, owner=created_by, created_by=created_by, ispublic=ispublic, description=description)
        organisation_instance.save()

        ''' Creates Organisation Member instance for the organisation owner '''
        OrganisationMember.objects.create(organisation=organisation_instance, user=created_by, role=3, invitation='accepted')

        return organisation_instance

class Organisation(models.Model):
    objects = OrganisationManager()

    owner = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, related_name='organisationowner', null=True)
    created_by = models.ForeignKey('CustomUser', editable=False, on_delete=models.SET_NULL, null=True)
    
    ispublic = models.BooleanField(default=True)
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to="organisation/", default="organisation/sustainability-circle.png", blank=True)
   
    class Meta:
        verbose_name = _('organisation')
        verbose_name_plural = _('organisations')

    def __str__(self):
        return self.name


'''
- m2m method_organisations/ESEA_Account class to add a campaign class to?)
- change ispublic to is_public
- M2m Esea Accounts required?
'''