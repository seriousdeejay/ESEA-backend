import unittest
from django.test import TestCase, Client

# Create your tests here.
class SimpleTest(TestCase):
    def test_details(self):
        response = self.client.get('/networks/')

        self.assertEqual(response.status_code, 200)

        # self.assertEqual(len(response.context['networks']))