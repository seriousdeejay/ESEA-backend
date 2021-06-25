from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import TextFragment, Section
from ..serializers import TextFragmentSerializer 

class TextFragmentViewSet(viewsets.ModelViewSet):
    serializer_class = TextFragmentSerializer

    def get_queryset(self):
        return TextFragment.objects.filter(section=self.kwargs['section_pk'])

    def create(self, request, method_pk, survey_pk, section_pk):
        section = get_object_or_404(Section, pk=section_pk)
        serializer = TextFragmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(section=section)

        return Response(serializer.data)