  
from django.test import Client, TestCase, SimpleTestCase
from django.urls import reverse , resolve
from ..views import networkview
from ..models import *

from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class TestCaseBase(TestCase):
    @property
    def bearer_token(self):
        # assuming there is a user in User model
        user = CustomUser.objects.create_user(username='testmin')
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION":f'Bearer {refresh.access_token}'}

class TestNetworks(TestCaseBase):
    def test_post_network(self):
        response = self.client.post(reverse('Networks-list'), data={"name": 'N1'}, **self.bearer_token, format="json")
        print(">> Network.POST:", response.content)
        # self.assertEqual(len(response.data), 1)

    def test_networks_url(self):
        response = self.client.get(reverse('Networks-list'), **self.bearer_token)
        print(">> Network.GET:", response.content)


        #request = self.factory.get('/networks/')
        #response = networkview.NetworkViewSet.as_view(request)
        #self.assertEqual(response.status_code, 200)

# self.client = Client()
# self.client.login(username='admin', password='admin')

# print('check')
# request = factory.get('/networks/')
# force_authenticate(request, user=user)
# response = networkview.NetworkViewSet.as_view(request)


# class TestUrls(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.client.login(username='admin', password='admin')

#     def test_networks_url_is_resolved(self):
#         response = self.client.get('/networks/')
#         print(response.status_code)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

        # url = reverse('networks')
        # self.assertEqual(resolve(url).)