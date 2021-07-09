from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from ..models import DirectIndicator
from ..serializers import DirectIndicatorSerializer2

class DirectIndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = DirectIndicatorSerializer2

    def get_queryset(self):
        return DirectIndicator.objects.filter(method=self.kwargs['method_pk'])
    
    def create(self, request, method_pk):
        request.data['method'] = int(method_pk)
        serializer = DirectIndicatorSerializer2(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)