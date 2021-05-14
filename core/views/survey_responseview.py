from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from secrets import token_urlsafe

from ..models import (Survey, SurveyResponse, QuestionResponse, DirectIndicator, IndirectIndicator, Respondent, StakeholderGroup, EseaAccount)
from ..serializers import (SurveyResponseSerializer, QuestionResponseSerializer, SurveyResponseCalculationSerializer)
from ..utils import map_responses_by_indicator, calculate_indicators

class BaseModelViewSet(viewsets.ModelViewSet):
    queryset = ''
    serializer_class = ''
    permission_classes = (AllowAny,)

    # Refer to https://stackoverflow.com/a/35987077/1677041
    permission_classes_by_action = {
        'create': permission_classes,
        'list': permission_classes,
        'retrieve': permission_classes,
        'update': permission_classes,
        'destroy': permission_classes,
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            if self.action:
                action_func = getattr(self, self.action, {})
                action_func_kwargs = getattr(action_func, 'kwargs', {})
                permission_classes = action_func_kwargs.get('permission_classes')
            else:
                permission_classes = None

            return [permission() for permission in (permission_classes or self.permission_classes)]

class SurveyResponseViewSet(BaseModelViewSet):
    serializer_class = SurveyResponseSerializer
    lookup_field = 'token'
    permission_classes_by_action = {
        'create': (IsAuthenticated,),
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'update': (AllowAny,),
        'destroy': (IsAuthenticated,),
        'all': (AllowAny,)
    }
    permission_classes = [AllowAny,]
    def get_queryset(self):
        print(self.kwargs)
        return SurveyResponse.objects.filter(esea_account=self.kwargs['esea_account_pk']) # finished=False
        
    def retrieve(self, request, network_pk, campaign_pk, esea_account_pk, token):
        if token == 'accountant':
            surveyresponse = get_object_or_404(SurveyResponse, survey__stakeholdergroup__name='accountant', esea_account=esea_account_pk)
        else:
            surveyresponse = get_object_or_404(SurveyResponse, token=token)
        print(surveyresponse)
        serializer = SurveyResponseSerializer(surveyresponse)
        return Response(serializer.data)
    
    def update(self, request, network_pk, campaign_pk, esea_account_pk, token):
        print('>>>>>', request.data)
        print(token)
        surveyresponse = get_object_or_404(SurveyResponse, token=token)
        serializer = SurveyResponseSerializer(surveyresponse, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    #@permission_classes(AllowAny,)
    def all(self, request, network_pk, campaign_pk, esea_account_pk):
        if True: #self.request.user.is_authenticated:
            eseaaccount = get_object_or_404(EseaAccount, pk=esea_account_pk)
            respondents = SurveyResponse.objects.filter(esea_account=esea_account_pk) #Respondent.objects.filter(organisation__esea_accounts=74)
            # print(respondents)
            responses = SurveyResponse.objects.filter(esea_account=esea_account_pk, finished=True)

            question_responses = QuestionResponse.objects.filter(survey_response__esea_account=esea_account_pk, survey_response__finished=True)
            # print(question_responses)

            indirect_indicators = IndirectIndicator.objects.filter(topic__method=eseaaccount.method)
            direct_indicators = DirectIndicator.objects.filter(topic__method=eseaaccount.method)
            
            # for item in question_responses:
            #     s = QuestionResponseSerializer(item, many=True)
          
            map_responses_by_indicator(direct_indicators, question_responses)
            indicators = calculate_indicators(indirect_indicators, direct_indicators)

            for indicator in indicators.values():
                #print(indicator.key, '---', indicator.value)
                if indicator.value is None:
                    print(indicator.key)                        
            serializer = SurveyResponseCalculationSerializer(indicators.values(), many=True)
            return Response(
                {
                    "respondents": len(respondents),
                    "responses": len(responses.filter(finished=True)),
                    "indics": [i.value for i in indicators.values()],
                    "indicators": serializer.data,
                    
                }
            )
        return Response({})
        

    @action(detail=True, methods=["get"])
    def calculations(self, request, organization_pk, method_pk, survey_pk, pk):
        survey_response = get_object_or_404(self.get_queryset(), pk=pk)
        indirect_indicators = IndirectIndicator.objects.filter(topic__method=method_pk)
        direct_indicators = survey_response.survey.questions.all()
        question_responses = survey_response.question_responses.all()
        
        map_responses_by_indicator(direct_indicators, question_responses)
        indicators = calculate_indicators(indirect_indicators, direct_indicators)
        serializer = SurveyResponseCalculationSerializer(indicators.values(), many=True)

        return Response(serializer.data)



# for di in direct_indicators:
#     print(di.key)
# serializer = SurveyResponseCalculationSerializer(direct_indicators, many=True)


# class PublicSurveyResponseViewset(viewsets.ModelViewSet):
#     serializer_class = SurveyResponseSerializer
#     authentication_classes = []
#     permission_classes = []

#     def get_queryset(self):
#         token = self.request.query_params.get("token")
#         return SurveyResponse.objects.filter(
#             survey=self.kwargs["survey_pk"],
#             user_organization=None,
#             token=token,
#         )

#     def perform_create(self, serializer):
#         token = self.request.query_params.get("token", token_urlsafe())
#         survey = get_object_or_404(Survey, pk=self.kwargs["survey_pk"])
#         serializer.save(survey=survey, token=token)

        # direct_indicator = get_object_or_404(DirectIndicator, pk=pk, topic__method=method_pk)
        # serializer = DirectIndicatorSerializer(direct_indicator, data=request.data)

    # def create(self, request, method_pk, survey_pk, organisation_pk):
    #     surveyresponse = SurveyResponse.objects.create(survey=request.data['survey'])
    #     serializer = SurveyResponseSerializer(surveyresponse)
    #     return Response(serializer.data)