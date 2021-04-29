from rest_framework import serializers

from ..models import Network, Organisation, Method
from .organisation import OrganisationSerializer


class NetworkSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    methods = serializers.StringRelatedField(many=True, read_only=True)
    organisations = serializers.SlugRelatedField(queryset=Organisation.objects.all(), many=True, required=False, slug_field='name')
    
    class Meta:
        model = Network
        fields = ['id', 'ispublic', 'name', 'description', 'created_by', 'organisations', 'methods']

    # methods = serializers.SlugRelatedField(queryset=Method.objects.all(), many=True, required=False, slug_field='id')
    # organisations = OrganisationSerializer(many=True, read_only=True)
    # ReadOnlyField(source="owner.username")
