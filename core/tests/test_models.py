from django.test import TestCase
from ..models import *

class NetworkTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Network.objects.create(name="My Network")

    def setUp(self):
        self.author = Network.objects.get(id=1)

    def test_name_label(self):
        print(self.respondent)
        field_label = Network._meta.get_field('name').verbose_name
        print('field_label:', field_label)

# class RespondentTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Respondent.objects.create(first_name="Henk")

#     def setUp(self):
#         self.respondent = Respondent.objects.get(id=1)

#     def test_name_label(self):
#         print(self.respondent)
#         field_label = Respondent._meta.get_field('first_name').verbose_name
#         print('field_label:', field_label)