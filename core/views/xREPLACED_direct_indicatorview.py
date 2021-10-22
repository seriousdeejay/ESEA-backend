# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404

# from ..models import DirectIndicator
# from ..serializers import DirectIndicatorSerializer


# class DirectIndicatorViewSet(viewsets.ViewSet):
#     def list(self, request, method_pk):
#         questions = DirectIndicator.objects.filter(topic__method=method_pk)
#         serializer = DirectIndicatorSerializer(questions, many=True)

#         return Response(serializer.data)
    
#     def create(self, request, method_pk):
#         request.data['method'] = int(method_pk)
#         serializer = DirectIndicatorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, method_pk, pk):
#         direct_indicator = get_object_or_404(DirectIndicator, pk=pk, topic__method=method_pk)
#         serializer = DirectIndicatorSerializer(direct_indicator)

#         return Response(serializer.data)

#     def update(self, request, method_pk, pk):
#         request.data['method'] = int(method_pk)
#         direct_indicator = get_object_or_404(DirectIndicator, pk=pk, topic__method=method_pk)
#         serializer = DirectIndicatorSerializer(direct_indicator, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data)
    
#     def destroy(self, request, method_pk, pk):
#         direct_indicator = get_object_or_404(DirectIndicator, pk=pk, topic__method = method_pk)
#         direct_indicator.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)