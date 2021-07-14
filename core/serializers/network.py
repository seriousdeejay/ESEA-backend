from rest_framework import serializers

from ..models import Network, Organisation, Method


class NetworkSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    campaigns = serializers.StringRelatedField(read_only=True, many=True)
    
    organisations = serializers.PrimaryKeyRelatedField(queryset=Organisation.objects.all(), many=True)
    
    methods = serializers.PrimaryKeyRelatedField(queryset=Method.objects.all(), many=True)
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = Network
        fields = ['id', 'ispublic', 'name', 'description', 'image', 'created_by', 'organisations', 'methods', 'campaigns']

    # organisations = serializers.SlugRelatedField(queryset=Organisation.objects.all(), many=True, required=False, slug_field='name')
    # methods = serializers.SlugRelatedField(queryset=Method.objects.all(), many=True, required=False, slug_field='name')
    #     print('Test')
    #     return instance
    # methods = serializers.SlugRelatedField(queryset=Method.objects.all(), many=True, required=False, slug_field='id')
    # organisations = OrganisationSerializer(many=True, read_only=True)
    # ReadOnlyField(source="owner.username")
