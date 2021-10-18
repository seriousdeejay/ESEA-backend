from rest_framework import serializers

from ..models import Network, NetworkMember, CustomUser, Organisation, Method


class NetworkSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    created_by_id = serializers.ReadOnlyField(source='created_by.id')
    owner = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username') # = networkadmin
    owner_id = serializers.ReadOnlyField(source='owner.id')
    campaigns = serializers.StringRelatedField(read_only=True, many=True)
    
    organisations = serializers.PrimaryKeyRelatedField(queryset=Organisation.objects.all(), many=True, required=False)
    methods = serializers.PrimaryKeyRelatedField(queryset=Method.objects.all(), many=True, required=False)
    
    class Meta:
        model = Network
        fields = ['id', 'ispublic', 'name', 'description', 'image', 'owner', 'owner_id', 'created_by', 'created_by_id', 'organisations', 'methods', 'campaigns']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user=self.context['request'].user

        # Sets acces level of user to the network
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















    # image = serializers.ImageField(required=False)
    # teammembers = serializers.StringRelatedField(read_only=True, many=True)
    # serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    # networkadmin = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, required=False)
    

    # def create(self, validated_data):
    #     try:
    #         owner = validated_data.pop('owner')
    #     except:
    #         owner = self.context['request'].user
            
    #     validated_data["owner"] = owner
        
    #     print(owner)
    #     # invitation='pending'
    #     # if owner.is_superuser:
        
    #     invitation='accepted'
    #     print(validated_data)
    #     network = Network.objects.create(**validated_data)
    #     return network

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
