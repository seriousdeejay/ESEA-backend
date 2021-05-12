from django.db import models
from django.utils.translation import gettext_lazy as _


class Network(models.Model):
    created_by = models.ForeignKey('CustomUser', editable=False, on_delete=models.SET_NULL, null=True)
    organisations = models.ManyToManyField('Organisation', related_name="networks", blank=True) 
    methods = models.ManyToManyField('Method', related_name="networks", blank=True)

    ispublic = models.BooleanField(default=True) # Change to is_public
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(blank=True, upload_to="network/", default="network/sustainability-circle.png")
    
    class Meta: 
        verbose_name = _('network')
        verbose_name_plural = _('networks')

    def __str__(self):
        return self.name

'''
- Should have a campaign?
- Should have image?
( - m2m network_methods class to add a campaign class to?)
'''