from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_if_register_endpoint_exists(self):
        self.assertEqual(self.client.get(self.url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)


