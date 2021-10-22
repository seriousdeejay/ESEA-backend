from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import NetworkMember, Network
from ..serializers import NetworkMemberSerializer



class NetworkMemberViewSet(viewsets.ModelViewSet):
    serializer_class = NetworkMemberSerializer

    def get_queryset(self):
        return NetworkMember.objects.filter(network=int(self.kwargs['network_pk']))
    

    def create(self, request, network_pk):
        request.data['network'] = int(network_pk)
        serializer = NetworkMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def update(self, request, network_pk, *args, **kwargs):
        request.data['network'] = int(network_pk)
        instance = self.get_object()

        serializer = NetworkMemberSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Allows only one networkadmin to exist and changes network.owner to the new networkadmin
        if request.data['role'] == 2:
            OldNetworkAdmins = NetworkMember.objects.filter(network=network_pk, role=2).exclude(user=instance.user)
            if len(OldNetworkAdmins):
                for admin in OldNetworkAdmins:
                    print(admin)
                    admin.role = 1
                    admin.save()
                
                network = Network.objects.get(id=network_pk)
                network.owner = instance.user
                network.save()

        return Response(serializer.data)










    # def perform_create(self, serializer):
    #     print('test')
    #     serializer.save()

    # return super().update(request, *args, **kwargs)

    # def retrieve(self, instance, network_pk, pk):
    #     i = get_object_or_404(NetworkMember, pk=pk)
    #     print(type(i.role))
    #     return Response({})