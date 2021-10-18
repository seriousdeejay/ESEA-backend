from rest_framework import viewsets
from rest_framework.response import Response

from ..models import OrganisationMember, Organisation
from ..serializers import OrganisationMemberSerializer

class OrganisationMemberViewSet(viewsets.ModelViewSet):
    serializer_class=OrganisationMemberSerializer

    def get_queryset(self):
        return OrganisationMember.objects.filter(organisation=int(self.kwargs['organisation_pk']))

    def create(self, request, organisation_pk):
        request.data['organisation'] = int(organisation_pk)
        serializer = OrganisationMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def update(self, request, organisation_pk, *args, **kwargs):
        request.data['organisation'] = organisation_pk
        instance = self.get_object()

        serializer = OrganisationMemberSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if request.data['role'] == 3:
            oldOrganisationAdmins = OrganisationMember.objects.filter(organisation=organisation_pk, role=3).exclude(user=instance.user)
            if len(oldOrganisationAdmins):
                for admin in oldOrganisationAdmins:
                    admin.role = 1
                    admin.save()
                
                organisation = Organisation.objects.get(id=organisation_pk)
                organisation.owner = instance.user
                organisation.save()

        return Response(serializer.data)
