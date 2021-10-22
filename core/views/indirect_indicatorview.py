from rest_framework import viewsets
from rest_framework.response import Response

from ..models import IndirectIndicator
from ..serializers import IndirectIndicatorSerializer



class IndirectIndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndirectIndicatorSerializer

    def get_queryset(self):
        return IndirectIndicator.objects.filter(method=self.kwargs['method_pk'])
    

    def create(self, request, method_pk):
        request.data['method'] = int(method_pk)
        serializer = IndirectIndicatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)





        # request.data['method'] = int(method_pk)
        # return super().create(request, method_pk)

    # def update(self, request, method_pk, pk):
    #     request.data['method'] = int(method_pk)
    #     return super().update(request, method_pk, pk)

    # def patch(self, request, method_pk, pk):
    #     request.data['method'] = int(method_pk)
    #     indicator = self.get_object()
    #     print('---->', request.data)
    #     serializer = IndirectIndicatorSerializer(indicator, data=request.data)#IndirectIndicatorSerializer(indicator, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


        # def get_serializer_class(self, *args, **kwargs):
    #     serializer_class = self.get_serializer_class()
    #     kwargs["context"] = self.get_serializer_context()
    #     draft_request_data = self.request.data.copy()
    #     draft_request_data['method'] = 