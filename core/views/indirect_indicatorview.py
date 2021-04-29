from rest_framework import viewsets
from ..models import IndirectIndicator
from ..serializers import IndirectIndicatorSerializer

class IndirectIndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndirectIndicatorSerializer

    def get_queryset(self):
        return IndirectIndicator.objects.filter(topic__method=self.kwargs['method_pk'])
    
    def create(self, request, method_pk):
        request.data['method'] = int(method_pk)
        return super().create(request, method_pk)

    def update(self, request, method_pk, pk):
        request.data['method'] = int(method_pk)
        return super().update(request, method_pk, pk)
