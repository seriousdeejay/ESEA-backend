from rest_framework.response import Response 
from rest_framework import viewsets, response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

import os
import yaml

from ..models import Method, Organisation, CustomUser, Topic, DirectIndicator, IndirectIndicator, Survey
from ..serializers import MethodSerializer, SurveyResponseCalculationSerializer
from ..utils import process_yaml_method, merge_indicators


class MethodViewSet(viewsets.ModelViewSet):
    serializer_class = MethodSerializer

    def get_queryset(self):
        network = self.request.GET.get('network', None)
        organisation = self.request.GET.get('organisation', None)
        excludenetwork = self.request.GET.get('excludenetwork', None)
        if network is not None:
            return Method.objects.filter(networks=network)
        if excludenetwork is not None:
            return Method.objects.exclude(networks=excludenetwork)
        if organisation is not None:
            return Method.objects.filter(organisations=organisation).distinct()

        return Method.objects.filter(Q(created_by=self.request.user) | Q(ispublic = True))

    def create(self, serializer):
        print(self.request.data)
        serializer = MethodSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        print('check')
        serializer.save(created_by=self.request.user)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        method_object = get_object_or_404(Method, pk=self.get_object().id)
        for instance in request.data:
            try:
                organisation = get_object_or_404(Organisation, id=instance['id'])
                if method_object.organisations.filter(id=organisation.id).exists():
                    method_object.organisations.remove(organisation)
                else:
                    method_object.organisations.add(organisation)
            except Exception as e:
                print('%s (%s)' % (e.message, type(e)))
        serializer = MethodSerializer(method_object)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def indicators(self, request):
        method = self.request.GET.get('method', None)
        print(method)
                # eseaaccount = get_object_or_404(EseaAccount, pk=esea_account_pk)
                # respondents = SurveyResponse.objects.filter(esea_account=esea_account_pk) #Respondent.objects.filter(organisation__esea_accounts=74)
                # # print(respondents)
                # responses = SurveyResponse.objects.filter(esea_account=esea_account_pk, finished=True)

                # question_responses = QuestionResponse.objects.filter(survey_response__esea_account=esea_account_pk, survey_response__finished=True)
                # # print(question_responses)

        indirect_indicators = IndirectIndicator.objects.filter(topic__method=method)
        direct_indicators = DirectIndicator.objects.filter(topic__method=method)
                
                # for item in question_responses:
                #     s = QuestionResponseSerializer(item, many=True)
            
                # for di in direct_indicators:
                #     print(di.key)
                #serializer = SurveyResponseCalculationSerializer(direct_indicators, many=True)
        indicators = merge_indicators(direct_indicators, indirect_indicators) #calculate_indicators(indirect_indicators, direct_indicators)
        print(indicators)
        # for indicator in indicators.values():
        #             #print(indicator.key, '---', indicator.value)
        #             if indicator.value is None:
        #                 print(indicator.key)                        
        serializer = SurveyResponseCalculationSerializer(indicators.values(), many=True)
        return Response({ "indicators": serializer.data })

@method_decorator(csrf_exempt, name='dispatch')
@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def upload_yaml(request):
    if request.method == 'POST':
    # if request.method == 'POST' and 'file' in request.FILES.keys():
        # with open(request.FILES['file'], encoding='utf-8') as file:
        with open(os.path.join(os.getcwd(), "core\\uploadedfiles\\newmethod2.yaml"), encoding='utf-8') as file:
            YAML_dict = yaml.safe_load(file)
            method_instance, errors = process_yaml_method(YAML_dict)
            if len(errors):
               return Response({'errors': errors})
            
            serializer = MethodSerializer(method_instance)
            return Response(serializer.data)


    '''
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        ##Try/Except to catch YAML related errors
        try:
            YAML_dict = yaml.safe_load(myfile)
            print(YAML_dict)
        except:
            pass
            
            currentuser = CustomUser.objects.get(id=1)
            m = Method.objects.create(name="BIA", description="A Method description", created_by=currentuser)
            topic_dict = {}

            ##Saving Topics
            for topic_key in YAML_dict['topics']:
                topic=YAML_dict['topics'][topic_key]
                description = None
                name=topic['name']
                if 'description' in topic.keys():
                    description = topic['description']
                if not 'topic' in topic.keys():
                    supertopic = Topic.objects.create(name=name, description=description, parent_topic=None, method=m)
                    topic_dict[topic_key] = supertopic
                else:            
                    subtopic = Topic.objects.create(name=name, description=description, parent_topic=topic_dict[topic['topic']], method=m)
                    topic_dict[topic_key] = subtopic
                    print(topic_key, subtopic)

            ##Saving Surveys
            for survey in YAML_dict['surveys']:
                YAML_dict['surveys'][survey]
                descriptiom, welcomeText, closingText = None, None, None
                name = YAML_dict['surveys'][survey]['name']
                responserate = YAML_dict['surveys'][survey]['responserate']
                if 'description' in YAML_dict['surveys'][survey].keys():
                    description = YAML_dict['surveys'][survey]['description']
                if 'welcometext' in YAML_dict['surveys'][survey].keys():
                    welcomeText = YAML_dict['surveys'][survey]['welcometext']
                if 'closingtext' in YAML_dict['surveys'][survey].keys():
                    closingText = YAML_dict['surveys'][survey]['closingtext']
                s = Survey.objects.create(name=name, description=description, anonymous=False, method=m)
                ##Saving Questions
                for question in YAML_dict['surveys'][survey]['questions']:
                    question = YAML_dict['surveys'][survey]['questions'][question]
                    isMandatory, description, instruction, options = True, None, None, None
                    try:
                        key = question['indicator']
                        topic = topic_dict[question['topic']]
                        answertype = question['answertype']
                        name = question['name']
                        if question['ismandatory'] == "N":
                            isMandatory = False
                        if 'description' in question.keys():
                            description = question['description']
                        if question['answertype'] == "RADIO":
                            options = question['options']
                        if question['answertype'] == "multipleChoice":
                            answertype = "CHECKBOX"
                            options = question['aggregatedqs']
                        q = DirectIndicator.objects.create(key=key, topic=topic, answertype=answertype, name=name, isMandatory=isMandatory, description=description, instruction=instruction, options=options)
                        s.questions.add(q)
                    except Exception as e:
                        print('%s (%s)' % (e.message, type(e)))
            return Response({"Method Saved!"})
        except yaml.YAMLError as exc:
            print(exc)
            return Response({exc})
            ## print('>>', q, 'TOPIC:', q.topic, q.question.options.all())
        '''
