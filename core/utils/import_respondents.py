from django_backend.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import csv
import io

from ..models import Respondent, SurveyResponse

def import_respondents(excel_file, eseaaccount, survey):
    decoded_file = excel_file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)

    colsdict = {}
    respondents = []
    requiredattributes = {'email', 'first_name', 'last_name', 'last_name_prefix'}

    for i, row in enumerate(csv.reader(io_string, delimiter=',', quotechar='|')):
        if (i == 0):
            row = [x.lower() for x in row]
            print(row)
            missingattributes = requiredattributes.difference(set(row))
            
            if missingattributes:
                return "Your csv file is missing the following attribute columns: " + ", ".join(missingattributes)
            for j, column in enumerate(row):
                colsdict[column] = j
        else:
            try:
                email =row[colsdict['email']]
                firstname = row[colsdict['first_name']]
                lastnameprefix = row[colsdict['last_name_prefix']]
                lastname = row[colsdict['last_name']]
                respondent = Respondent(organisation=eseaaccount.organisation, email=email, first_name=firstname, last_name_prefix=lastnameprefix, last_name=lastname)
                print(respondent)
                respondents.append(respondent)
            except:
                return f"error in row {i}: {row}"
    for respondent in respondents:
        respondent.save()
        new_survey_response = SurveyResponse.objects.create(survey=survey, respondent=respondent, esea_account=eseaaccount)
        print(f'{respondent}: {new_survey_response.token}')
        subject = f"Survey for {respondent} regarding {respondent.organisation}"
        message = f"Hi {respondent}!\nWe would like you to take a moment to fill in the following survey as employee of {respondent.organisation} to create a report about the organisation's position in the ethical, social and environmental fields.\n\n https://esea.herokuapp.com/survey-fill/{new_survey_response.token}/" # http://localhost:8080/
        # recepient = respondent.email
        recepient = "seriousdeejay@gmail.com"
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        break
    return "The Survey has been succesfully deployed to the provided survey respondents."























'''
    eseaaccount = get_object_or_404(EseaAccount, pk=eseaaccount_pk)
    colsdict = {}
    requiredattributes = {'email', 'first_name', 'last_name', 'last_name_prefix'}
    respondents = []

    with open(os.path.join(os.getcwd(), "core\\uploadedfiles\\uploadedemployees.csv")) as file:
         #maybe quotechar should be , ?
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