from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404

from ..models import Topic, Method
from ..serializers import TopicSerializer



class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer

    def get_queryset(self):
        return Topic.objects.filter(method=self.kwargs['method_pk']) 


    def perform_create(self, serializer):
        method = get_object_or_404(Method, pk=self.kwargs['method_pk'])
        serializer.save(method=method)






    # def create(self, serializer, method_pk):
    #     print(self.request.data)
    #     method = get_object_or_404(Method, pk=self.kwargs['method_pk'])
    #     serializer = TopicSerializer(data=self.request.data)
    #     if serializer.is_valid():
    #         serializer.save(method=method)
    #         return Response(serializer.data)

    # return Response(serializer.data, status=status.HTTP_201_CREATED)

    # {
    #     "name": "Topic 9",
    #     "description": "",
    #     "parent_topic": null   == Optional
    # }