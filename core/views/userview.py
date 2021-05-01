from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from ..serializers import RegisterUserSerializer, UserSerializer
from ..models import CustomUser, Organisation, StakeholderGroup, Respondent, SurveyResponse

import os
import csv
import string
import random


class RegisterUserView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterUserSerializer

class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    model = CustomUser
    serializer_class = UserSerializer

    def get_queryset(self):
        currentuser = self.request.GET.get('currentuser', None)
        network = self.request.GET.get('network', None)
        organisation = self.request.GET.get('organisation', None)

        if currentuser is not None:
            return CustomUser.objects.filter(id=self.request.user.id)
        if network is not None:
            return CustomUser.objects.filter(organisation__networks=network).distinct() # Should pass network id(s) in order to serve the participants of network(s)
        if organisation is not None:
            return CustomUser.objects.filter(organisation=organisation)
        return CustomUser.objects.all()

'''
@method_decorator(csrf_exempt, name='dispatch')
@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def import_employees(request, organisation_pk):
    if request.method == 'POST' and 'file' in request.FILES.keys():
        myfile = request.FILES['file']
    organisation = get_object_or_404(Organisation, pk=organisation_pk)
    colsdict = {}
    requiredattributes = {'email', 'first_name', 'last_name', 'last_name_prefix'}
    respondents = []

    with open(os.path.join(os.getcwd(), "core\\uploadedfiles\\uploadedemployees.csv")) as file:
        newemployees = csv.reader(file, delimiter=",", quotechar="|") #maybe quotechar should be , ?
        for i, row in enumerate(newemployees):
            print(row)
            if (i == 0):
                missingattributes = requiredattributes.difference(set(row))
                if missingattributes:
                    responsestring = "Your csv file is missing the following attribute columns: " + ", ".join(missingattributes)
                    return Response({responsestring})
                for j, column in enumerate(row):
                    colsdict[column] = j

            else:
                try:
                    email = row[colsdict['email']]
                    firstname = row[colsdict['first_name']]
                    lastnameprefix = row[colsdict['last_name_prefix']]
                    lastname = row[colsdict['last_name']]
                    respondent = Respondent(organisation=organisation, email=email, first_name=firstname, last_name_prefix=lastnameprefix, last_name=lastname)
                    print(i, '--------', respondent)
                    respondents.append(respondent)
                except:
                    return Response({f"error in row {i}"})

    Respondent.objects.all().delete()
    # for respondent in respo
    #Respondent.objects.create(respondents)
    #respondentss = Respondent.objects.all().first()
    print(respondents)
    for respondent in respondents:
        respondent.save()
        print(respondent.id)
        print(Respondent.objects.all().first().id)
        new_survey_response = SurveyResponse.objects.create(survey=1, respondent=respondent)
        subject = f"Survey for {respondent} regarding {respondent.organisation}"
        message = f"Hi {respondent}!\nWe would like you to take a moment to fill in the following survey as employee of {respondent.organisation} to create a report about the organisation's position in the ethical, social and environmental fields.\n\nhttp://localhost:8080/{new_survey_response.token}/"
        #recepient = respondent.email
        recepient = "seriousdeejay@gmail.com"
        # send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    return Response({"The Survey has been succesfully deployed to the provided survey respondents."})

                        # data = { "email": email, "first_name": firstname, "last_name_prefix": lastnameprefix, "last_name": lastname, "username": username, "password": password, "password2": password, "uniquetoken": password}
                    # print(data)
                    # serializer = RegisterUserSerializer(data=data)
                    # serializer.is_valid(raise_exception=True)
                    # print(serializer.data)
                    # serializer.save()
                    # newuser = get_object_or_404(CustomUser, username=serializer.data['username'])
                    # print(newuser)
                    # userorganisation = UserOrganisation.objects.create(user=newuser, organisation=organisation)
                    # stakeholdergroup = StakeholderGroup.objects.get(name="Employee")
                    # userorganisation.stakeholdergroups.add(stakeholdergroup)
                    # userorganisation.save()
                    # serializer = UserSerializer(newuser  
                
'''