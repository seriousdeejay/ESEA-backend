from rest_framework import serializers

from ..models import OrganisationMember, CustomUser


class OrganisationMemberSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='get_role_display', required=False)
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = OrganisationMember
        fields = ['id', 'invitation', 'role', 'role_name', 'organisation', 'user', 'user_name']




    






# user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())