from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from ..models import Membership
from ..serializers import MembershipSerializer

class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipSerializer

    def get_queryset(self):
        network = self.request.GET.get('network', None)
        organisation = self.request.GET.get('organisation', None)

        if network is not None:
            return Membership.objects.filter(network=network, status="pending")
        if organisation is not None:
            return Membership.objects.filter(organisation=organisation)
        return Membership.objects.all()
    
    # def create(self, request, method_pk):
    #     request.data['method'] = int(method_pk)
    #     serializer = DirectIndicatorSerializer2(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data)