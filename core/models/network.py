from django.db import models
from django.utils.translation import gettext_lazy as _

from .network_member import NetworkMember


class NetworkManager(models.Manager):
    def create(self, name, owner, created_by, ispublic=True, description="", organisations=[], methods=[]):

        network_instance = Network(name=name, ispublic=ispublic, description=description, owner=owner, created_by=created_by)
        network_instance.save()
        
        ''' Creates Network Member instance for the network owner '''
        NetworkMember.objects.create(network=network_instance, user=owner, role=2, invitation='accepted')

        return network_instance

class Network(models.Model):
    objects = NetworkManager()
    
    owner = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, related_name="networkowner", null=True)
    created_by = models.ForeignKey('CustomUser', editable=False, on_delete=models.SET_NULL, null=True)
    organisations = models.ManyToManyField('Organisation', related_name="networks", blank=True) 
    methods = models.ManyToManyField('Method', related_name="networks", blank=True)

    ispublic = models.BooleanField(default=True) 
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to="network/", default="network/sustainability-circle.png")
    
    class Meta: 
        verbose_name = _('network')
        verbose_name_plural = _('networks')

    def __str__(self):
        return self.name










'''
- Change ispublic to is_public?
'''