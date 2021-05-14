
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ..models import EseaAccount, Survey, Respondent, SurveyResponse
from ..serializers import EseaAccountSerializer
from ..utils import import_respondents


class EseaAccountViewSet(viewsets.ModelViewSet):
    serializer_class = EseaAccountSerializer

    def get_queryset(self):
        organisation = self.request.GET.get('organisation', None)
        if organisation is not None:
            return EseaAccount.objects.filter(organisation=organisation)
        return EseaAccount.objects.filter(campaign = self.kwargs['campaign_pk'])

    def create(self, request, campaign_pk, *args, **kwargs):
       request.data['campaign'] = campaign_pk
       return super().create(request, *args, **kwargs)

    def update(self, request, campaign_pk, *args, **kwargs):
        request.data['campaign'] = campaign_pk
        return super().update(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def import_employees(request, eseaaccount_pk, survey_pk):
    if request.method == 'POST' and request.FILES.get('file', False): # and 'file' in request.FILES.keys(): # and 
        
        
        eseaaccount = get_object_or_404(EseaAccount, pk=eseaaccount_pk)
        survey = get_object_or_404(Survey, pk=survey_pk)

        Respondent.objects.filter(organisation=eseaaccount.organisation).delete()
        SurveyResponse.objects.filter(survey=survey_pk, esea_account=eseaaccount_pk)

        file = request.FILES['file']

        if file.size > 1000000:
            return Response({f'File is larger than 1MB. {file.size}'})
        
        # TODO magic.from_buffer() to validate that uploaded file is actually a csv file.

        output = import_respondents(file, eseaaccount, survey)
        print(output)
        return Response({output})
    return Response({'No Excel file uploaded'})

    '''
    eseaaccount = get_object_or_404(EseaAccount, pk=eseaaccount_pk)
    colsdict = {}
    requiredattributes = {'email', 'first_name', 'last_name', 'last_name_prefix'}
    respondents = []

    with open(os.path.join(os.getcwd(), "core\\uploadedfiles\\uploadedemployees.csv")) as file:
        newemployees = csv.reader(file, delimiter=",", quotechar="|") #maybe quotechar should be , ?
        for i, row in enumerate(newemployees):
            if (i == 0):
                missingattributes = requiredattributes.difference(set(row))
                if missingattributes:
                    responsestring = "Your csv file is missing the following attribute columns: " + ", ".join(missingattributes)
                    return Response({responsestring})
                for j, column in enumerate(row):
                    colsdict[column] = j

            else:
                try:
                    print(eseaaccount.organisation)
                    email = row[colsdict['email']]
                    firstname = row[colsdict['first_name']]
                    lastnameprefix = row[colsdict['last_name_prefix']]
                    lastname = row[colsdict['last_name']]
                    print('ch')
                    respondent = Respondent(organisation=eseaaccount.organisation, email=email, first_name=firstname, last_name_prefix=lastnameprefix, last_name=lastname)
                    print(i, '--------', respondent)
                    respondents.append(respondent)
                except:
                    return Response({f"error in row {i}"})

    for respondent in respondents:
        respondent.save()
        new_survey_response = SurveyResponse.objects.create(survey=1, respondent=respondent, esea_account=eseaaccount)
        subject = f"Survey for {respondent} regarding {respondent.organisation}"
        message = f"Hi {respondent}!\nWe would like you to take a moment to fill in the following survey as employee of {respondent.organisation} to create a report about the organisation's position in the ethical, social and environmental fields.\n\nhttp://localhost:8080/{new_survey_response.token}/"
        #recepient = respondent.email
        recepient = "seriousdeejay@gmail.com"
        # send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    return Response({"The Survey has been succesfully deployed to the provided survey respondents."})
    '''

        # def create(self, serializer, network_pk, campaign_pk):
    #     print('>>>>', self.request.data)
    #     serializer = EseaAccountSerializer(data=self.request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # goes to serializer def create()
    #     return Response(serializer.data)


    # def update(self, request, network_pk, campaign_pk, pk):
    #     esea_account = get_object_or_404(EseaAccount, pk=pk)
    #     serializer = EseaAccountSerializer(esea_account, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     print(esea_account.sufficient_response_rate()) # Maybe i have to put this in the serializer update method? If sufficient_response_rate gets returned a report can be created
    #     return Response(serializer.data)