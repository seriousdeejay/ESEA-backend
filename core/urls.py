from django.urls import path, include, re_path
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from .views import (respondentview, userview, networkview, organisationview, methodview, surveyview, topicview, direct_indicatorview, indirect_indicatorview, survey_responseview, campaignview, esea_accountview)
 

router = routers.DefaultRouter()
router.register(r'respondents', respondentview.RespondentsViewSet, basename="Respondents")
router.register(r'users', userview.UsersViewSet, basename="Users")
router.register(r'networks', networkview.NetworkViewSet, basename="Networks")
router.register(r'organisations', organisationview.OrganisationViewSet, basename="Organisations")
router.register(r'methods', methodview.MethodViewSet, basename='methods')   ## /methods/ & /methods/{pk}/

network_router = routers.NestedSimpleRouter(router, r'networks', lookup="network")
network_router.register(r'campaigns', campaignview.CampaignViewSet, basename="network-campaigns" )

campaign_router = routers.NestedSimpleRouter(network_router, r'campaigns', lookup="campaign")
campaign_router.register(r'esea-accounts', esea_accountview.EseaAccountViewSet, basename="campaign-esea-accounts")

esea_account_router = routers.NestedSimpleRouter(campaign_router, r'esea-accounts', lookup="esea_account")
esea_account_router.register(r'responses', survey_responseview.SurveyResponseViewSet, basename='esea-account-responses')

method_router = routers.NestedSimpleRouter(router, r'methods', lookup="method")
method_router.register(r'surveys', surveyview.SurveyViewSet, basename="method-surveys")
method_router.register(r'topics', topicview.TopicViewSet, basename="method-topics")     ## /methods/{pk}/topics & /methods/{pk}/topics/{pk}/
method_router.register(r'questions', direct_indicatorview.DirectIndicatorViewSet, basename="method-questions")
method_router.register(r'indirect-indicators', indirect_indicatorview.IndirectIndicatorViewSet, basename="method-indirect-indicators")

survey_router = routers.NestedSimpleRouter(method_router, r'surveys', lookup="survey")
survey_router.register(r'organisations', organisationview.OrganisationViewSet, basename="survey-organisations")

#organisation_router = routers.NestedSimpleRouter(survey_router, r'organisations', lookup="organisation")
#organisation_router.register(r'responses', survey_responseview.SurveyResponseViewSet, basename="organisation-responses")

# router.register(r'topics', topicview.TopicViewSet, basename='topics')
# router.register(r'questions', direct_indicatorview.DirectIndicatorViewSet, basename='questions')
# router.register(r'surveys', surveyview.SurveyViewSet, basename='surveys')
router.register(r'public-surveys', surveyview.PublicSurveyViewSet, basename='public-surveys')
# router.register(r'personalorganisations', organisationview.PersonalOrganisationViewSet, basename='Organisation')


urlpatterns = [
    path('account/register/', userview.RegisterUserView.as_view(), name='user_registration'),
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-refresh/', TokenRefreshView.as_view()),
    path('import-yaml/', methodview.upload_yaml),
    path('import-employees/<int:eseaaccount_pk>/<int:survey_pk>/', esea_accountview.import_employees, name="import_employees_of_organisation"),
    path('send-surveys/', organisationview.send_surveys, name="send_surveys_to_emails"),
    path('', include(router.urls)),
    path('', include(network_router.urls)),
    path('', include(campaign_router.urls)),
    path('', include(method_router.urls)),
    path('', include(survey_router.urls)),
    path('', include(esea_account_router.urls))
    #path('', include(organisation_router.urls)),
]




    # path('organisationparticipants/<int:pk>/', organisationview.OrganisationParticipantsViewSet.as_view({'get': 'list'})),
    # path('networkorganisations/<int:pk>/', networkview.NetworkOrganisationsViewSet.as_view({'get': 'list'}))