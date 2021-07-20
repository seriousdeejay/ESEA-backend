from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.shortcuts import get_object_or_404

from ..models import NetworkMember
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

    def perform_create(self, serializer):
        print('test')
        serializer.save()

    def update(self, request, network_pk, *args, **kwargs):
        request.data['network'] = network_pk
        return super().update(request, *args, **kwargs)

    def retrieve(self, instance, network_pk, pk):
        i = get_object_or_404(NetworkMember, pk=pk)
        print(type(i.role))
        return Response({})