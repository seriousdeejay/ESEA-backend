from rest_framework import viewsets
from rest_framework.response import Response

from ..models import OrganisationMember
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
        return super().update(request, *args, **kwargs)