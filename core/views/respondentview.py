from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Respondent
from ..serializers import RespondentSerializer



class RespondentsViewSet(viewsets.ModelViewSet):
    model = Respondent
    serializer_class = RespondentSerializer

    def get_queryset(self):
        organisation = self.request.GET.get('organisation', None)
        if organisation is not None:
            return Respondent.objects.filter(organisation=organisation)
        return Respondent.objects.all()