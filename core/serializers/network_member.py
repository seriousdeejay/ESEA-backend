from rest_framework import serializers

from ..models import NetworkMember, CustomUser

class NetworkMemberSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='get_role_display', required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = NetworkMember
        fields = ['id', 'invitation', 'role', 'role_name', 'network', 'user', 'user_name']
    
    # def update(self, instance, validated_data):

    #     return instance