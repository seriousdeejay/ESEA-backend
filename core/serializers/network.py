from rest_framework import serializers

from ..models import Network, CustomUser, Organisation, Method


class NetworkSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField() # serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    created_by_id = serializers.ReadOnlyField(source='created_by.id')
    campaigns = serializers.StringRelatedField(read_only=True, many=True)
    
    organisations = serializers.PrimaryKeyRelatedField(queryset=Organisation.objects.all(), many=True, required=False)
    methods = serializers.PrimaryKeyRelatedField(queryset=Method.objects.all(), many=True, required=False)
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = Network
        fields = ['id', 'ispublic', 'name', 'description', 'image', 'created_by', 'created_by_id', 'organisations', 'methods', 'campaigns']

    # def update(self, instance, validated_data):
    #     print('check')
    #     print(validated_data)
    #     return instance
    # organisations = serializers.SlugRelatedField(queryset=Organisation.objects.all(), many=True, required=False, slug_field='name')
    # methods = serializers.SlugRelatedField(queryset=Method.objects.all(), many=True, required=False, slug_field='name')
    #     print('Test')
    #     return instance
    # methods = serializers.SlugRelatedField(queryset=Method.objects.all(), many=True, required=False, slug_field='id')
    # organisations = OrganisationSerializer(many=True, read_only=True)
    # ReadOnlyField(source="owner.username")
