from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from ..models import Campaign
from ..serializers import CampaignSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer

    def get_queryset(self):
        if  self.kwargs['network_pk'] == 0: # 
            return Campaign.objects.all()
        return Campaign.objects.filter(network=self.kwargs['network_pk'])

    # def create(self, request, network_pk, *args, **kwargs):
    #    request.data['network'] = network_pk
    #    print('----------', request.data)
    #    return super().create(request, *args, **kwargs)
    
    def create(self, request, network_pk):
        request.data['network'] = int(network_pk)
        serializer = CampaignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def update(self, request, network_pk, *args, **kwargs):
        request.data['network'] = network_pk
        return super().update(request, *args, **kwargs)

    # def create(self, request, network_pk):
    #    request.data['network'] = int(network_pk)
    #    print('network: ', network_pk)
    #    serializer = CampaignSerializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    serializer.save()
    #    return Response(serializer.data)

    # def update(self, request, network_pk, pk):
    #     request.data['network'] = int(network_pk)
    #     campaign = get_object_or_404(Campaign, pk=pk)
    #     serializer = CampaignSerializer(campaign, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
