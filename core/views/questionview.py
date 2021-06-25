from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Question
from ..serializers import QuestionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        print(self.kwargs['section_pk'])
        return Question.objects.filter(section=self.kwargs['section_pk'])
    
    def create(self, request, method_pk, survey_pk, section_pk):
        request.data['section'] = int(section_pk)
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    