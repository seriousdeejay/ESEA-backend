from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from ..models import Section
from ..serializers import SectionSerializer



class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer

    def get_queryset(self):
        if (int(self.kwargs['survey_pk']) > 0):
            return Section.objects.filter(survey=self.kwargs['survey_pk'])
        return Section.objects.filter(survey__method=self.kwargs['method_pk'])
    
    def create(self, request, method_pk, survey_pk):
        request.data['survey'] = int(survey_pk)
        serializer = SectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)