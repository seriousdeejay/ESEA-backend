from rest_framework import serializers

from ..models import Membership

class MembershipSerializer(serializers.ModelSerializer):
    # organisation_name = serializers.ReadOnlyField(source="organisation.name")
    # organisation_description = serializers.ReadOnlyField(source="organisation.description")
    class Meta:
        model = Membership
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.requester == 'organisation':
            representation['organisation_name'] = instance.organisation.name
            representation['organisation_description'] = instance.organisation.description
        if instance.requester == 'network':
            representation['network_name'] = instance.network.name
            representation['network_description'] = instance.network.description
        return representation