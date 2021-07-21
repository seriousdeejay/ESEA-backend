from rest_framework import serializers

from ..models import Network, NetworkMember, CustomUser, Organisation, Method


class NetworkSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField() # serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    created_by_id = serializers.ReadOnlyField(source='created_by.id')
    # teammembers = serializers.StringRelatedField(read_only=True, many=True)
    campaigns = serializers.StringRelatedField(read_only=True, many=True)
    
    organisations = serializers.PrimaryKeyRelatedField(queryset=Organisation.objects.all(), many=True, required=False)
    methods = serializers.PrimaryKeyRelatedField(queryset=Method.objects.all(), many=True, required=False)
    image = serializers.ImageField(required=False)
    networkadmin = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, required=False)
    
    class Meta:
        model = Network
        fields = ['id', 'ispublic', 'name', 'description', 'image', 'created_by', 'created_by_id', 'organisations', 'methods', 'campaigns', 'networkadmin']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user=self.context['request'].user

        if user.is_superuser:
           representation['accesLevel'] = "admin"
        else:
            try:
                member = NetworkMember.objects.get(network=instance, user=user)
            except NetworkMember.DoesNotExist:
                member = None

            if member:
                representation['accesLevel'] = member.get_role_display()
        return representation

    def create(self, validated_data):
        networkadmin = validated_data.pop('networkadmin')

        if not networkadmin:
            networkadmin = self.context['request'].user
        
        invitation='pending'
        if networkadmin.is_superuser:
            invitation='accepted'

        network = Network.objects.create(**validated_data)

        NetworkMember.objects.create(network=network, user=networkadmin, role=2, invitation=invitation)
        return network

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
