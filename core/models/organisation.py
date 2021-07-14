from django.db import models
from django.utils.translation import gettext_lazy as _


class Organisation(models.Model):
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