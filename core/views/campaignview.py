from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from ..models import Campaign
from ..serializers import CampaignSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer

    def get_queryset(self):
        if self.kwargs['network_pk'] == 0:
            return Campaign.objects.all()
        return Campaign.objects.filter(network=self.kwargs['network_pk'])

    def create(self, serializer, network_pk):
        print(self.request.data)
        serializer = CampaignSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() # goes to serializer def create()
        return Response(serializer.data)

    def update(self, request, network_pk, pk):
        print(self.request.data)
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignSerializer(campaign, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)