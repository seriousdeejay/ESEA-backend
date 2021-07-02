from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q, Prefetch
from django.shortcuts import get_object_or_404
# from django_backend.settings import EMAIL_HOST_USER
# from django.core.mail import send_mail
# import base64

from ..models import Organisation
from ..serializers import OrganisationSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganisationSerializer
   
    def get_queryset(self):
        network = self.request.GET.get('network', None)
        excludenetwork = self.request.GET.get('excludenetwork', None)
        method = self.request.GET.get('method', None)
        excludemethod = self.request.GET.get('excludemethod', None)
        campaign = self.request.GET.get('campaign', None)
        excludecampaign = self.request.GET.get('excludecampaign', None)
        print(Organisation._meta.get_fields())
        if (network is not None) and (excludecampaign is not None):
            print('check')
            return Organisation.objects.filter(networks=network).exclude(esea_accounts__campaign=excludecampaign)
        if network is not None:
            if method is not None:
                return Organisation.objects.filter(networks=network, esea_accounts=method).distinct()
            if excludemethod is not None:
                return Organisation.objects.filter(networks=network).exclude(esea_accounts=excludemethod)
            return Organisation.objects.filter(networks=network)
        if excludenetwork is not None:
            return Organisation.objects.exclude(networks=excludenetwork)
        if campaign is not None:
            return Organisation.objects.filter(esea_accounts__campaign=campaign)
        return Organisation.objects.filter(Q(created_by=self.request.user) | Q(ispublic = True))
    
    def create(self, serializer):
        serializer = OrganisationSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data)

    # def update(self, request, pk):
    #     print(request.data)
    #     # request.data.pop('image')
    #     #image = base64.urlsafe_b64decode(request.data['image'])
    #     #request.data['image'] = image
    #     # print('>>', request.data['image']).decode("base64")
    #     #print('headers:', request.headers)
    #     print(request.FILES)
    #     organisation = get_object_or_404(Organisation, pk=pk)
    #     serializer = OrganisationSerializer(organisation, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def partial_update(self, request, *args, **kwargs):
    #     pass
        # Should be reworked

        # organisation_object = get_object_or_404(Organisation, pk=self.get_object().id)
        # data = request.data
        # try:
        #     for user in data:
        #         user = CustomUser.objects.get(id = user['id'])
        #         if organisation_object.members.filter(pk=user.pk).exists():                    
        #             organisation_object.members.remove(user)
        #         else:
        #             organisation_object.members.add(user)
        # except KeyError:
        #     pass
        # organisation_object.save()
        # serializer = OrganisationSerializer(organisation_object)
        # return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def send_surveys(request):
    pass
    # if request.method == 'POST':
    #     for surveyrespondent in request.data:
    #         print(surveyrespondent)
    #         subject = f"Survey for {user['user_organisations'][0]['organisation']}"
    #         message = f"Hi {user['first_name']} {user['last_name_prefix']} {user['last_name']}!\nWe would like you to take a moment to fill in the following survey as employee of {user['user_organisations'][0]['organisation']} to create a report about the organisation's position in the ethical, social and environmental fields.\n\nhttp://localhost:8080/{user['uniquetoken']}"
    #         recepient = "seriousdeejay@gmail.com"
    #         # send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    #         print(uo)
    #         #serializer = SurveyResponseSerializer(data = {survey: })
    #         newSurveyResponse = SurveyResponse.objects.create(survey=13,  user_organisation=uo.id)
    #         print(newSurveyResponse.__dict__)
    #     return Response({'Success'})
    # print('check')
    # return Response({'No Post Request'})

     #return Organisation.objects.prefetch_related(Prefetch('methods.surveys.responses', queryset=SurveyResponse.objects.filter(survey__method=method, survey__method__networks=network), to_attr='filtered_survey_responses'))