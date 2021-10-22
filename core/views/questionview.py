from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Question
from ..serializers import QuestionSerializer



class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        if (int(self.kwargs['survey_pk']) > 0) and (int(self.kwargs['section_pk']) > 0):
            return Question.objects.filter(section=self.kwargs['section_pk'])
        if (int(self.kwargs['survey_pk']) > 0):
            return Question.objects.filter(section__survey=self.kwargs['survey_pk'])
        return Question.objects.filter(method=self.kwargs['method_pk'])
        
    
    def create(self, request, method_pk, survey_pk, section_pk):
        if int(self.kwargs['method_pk']) > 0:
            request.data['method'] = int(method_pk)
        if int(self.kwargs['section_pk']) > 0:
            request.data['section'] = int(section_pk)
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    