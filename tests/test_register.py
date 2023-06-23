from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APITestCase

from achare_interview.utils.redis_client import validation_code_redis, reset_redis


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.authenticate_url = reverse('authenticate')
        self.validate_url = reverse('validate')
        self.register_url = reverse('register')

    def test_if_register_endpoint_exists(self):
        reset_redis(validation_code_redis)
        self.assertNotEqual(self.client.get(self.register_url).status_code, HTTPStatus.NOT_FOUND)

    def test_if_register_endpoint_method_type_is_post(self):
        reset_redis(validation_code_redis)
        self.assertEqual(self.client.get(self.register_url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertNotEqual(self.client.post(self.register_url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_if_register_checks_required_fields_are_sent_in_body(self):
        reset_redis(validation_code_redis)
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("phone_number", response.data.keys())
        self.assertIn("first_name", response.data.keys())
        self.assertIn("last_name", response.data.keys())

    # skipping phone_number tests because it got tested in test_authenticate test cases it'll be skipped here
    # skipping test_cases for first_name and last_name length because the same parameters are used in phone_number tests

    # def test_if_without_code_user_can_register
    # def test_for session