from django.db import models
from django.utils.translation import gettext_lazy as _


class Network(models.Model):
    created_by = models.ForeignKey('CustomUser', editable=False, on_delete=models.SET_NULL, null=True)
    organisations = models.ManyToManyField('Organisation', related_name="networks", blank=True) 
    methods = models.ManyToManyField('Method', related_name="networks", blank=True)

    ispublic = models.BooleanField(default=True) 
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to="network/", default="network/sustainability-circle.png", blank=True)
    
    class Meta: 
        verbose_name = _('network')
        verbose_name_plural = _('networks')

    def __str__(self):
        return self.name

'''
- Should use through class like below:
    --> esea_accounts = models.ManyToManyField('Method', through="EseaAccount", through_fields=('organisation', 'method'), related_name='organisations', blank=True)
( - m2m network_methods class to add a campaign class to?)
- Change ispublic to is_public
'''