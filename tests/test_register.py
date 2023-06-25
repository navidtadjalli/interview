from http import HTTPStatus
from uuid import uuid4

from django.urls import reverse
from rest_framework.test import APITestCase

from achare_interview.utils import error_messages
from achare_interview.utils.redis_utils import redis_client, key_generators
from customer.models import Customer


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.authenticate_url = reverse('authenticate')
        self.validate_url = reverse('validate')
        self.register_url = reverse('register')

        self.phone_number = "09123456789"
        self.code = self.phone_number[-6:]
        self.first_name = "first_name"
        self.last_name = "last_name"
        self.password = "password"
        self.sample_token = uuid4().hex

    def delete_redis(self):
        redis_client.reset_redis(redis_client.validation_code_redis)
        redis_client.reset_redis(redis_client.registration_token_redis)

    def test_if_register_endpoint_exists(self):
        self.delete_redis()
        self.assertNotEqual(self.client.get(self.register_url).status_code, HTTPStatus.NOT_FOUND)

    def test_if_register_endpoint_method_type_is_post(self):
        self.delete_redis()

        self.assertEqual(self.client.get(self.register_url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertNotEqual(self.client.post(self.register_url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_if_register_checks_required_fields_are_sent_in_body(self):
        self.delete_redis()
        response = self.client.post(self.register_url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("phone_number", response.data.keys())
        self.assertIn("first_name", response.data.keys())
        self.assertIn("last_name", response.data.keys())
        self.assertIn("registration_token", response.data.keys())
        self.assertIn("password", response.data.keys())

    # skipping phone_number tests because it got tested in test_authenticate test cases it'll be skipped here

    def test_if_register_has_blank_for_first_name_and_last_name(self):
        self.delete_redis()
        response = self.client.post(self.register_url, data={
            "phone_number": self.phone_number,
            "first_name": '',
            "last_name": '',
            "registration_token": self.sample_token,
            "password": self.password
        })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)

    def test_if_register_has_minimum_length_for_first_name_and_last_name(self):
        self.delete_redis()
        response = self.client.post(self.register_url, data={
            "phone_number": self.phone_number,
            "first_name": 'a',
            "last_name": 'a',
            "registration_token": self.sample_token,
            "password": self.password
        })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)

    def test_if_register_has_maximum_length_for_first_name_and_last_name(self):
        self.delete_redis()
        response = self.client.post(self.register_url, data={
            "phone_number": self.phone_number,
            "first_name": "a" * 151,
            "last_name": "a" * 151,
            "registration_token": self.sample_token,
            "password": self.password
        })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)

    def test_if_register_validates_length_of_registration_token(self):
        self.delete_redis()
        response = self.client.post(self.register_url, data={
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "registration_token": "1" * 31,
            "password": self.password
        })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("registration_token", response.data)

        response = self.client.post(self.register_url, data={
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "registration_token": "1" * 33,
            "password": self.password
        })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("registration_token", response.data)

    def test_if_register_checks_registration_token(self):
        self.delete_redis()

        response = self.client.post(self.register_url, data={
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "registration_token": self.sample_token,
            "password": self.password
        })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, error_messages.REGISTRATION_TOKEN_IS_NOT_VALID_ERROR_MESSAGE)

    def test_if_register_checks_registration_token_value_from_redis(self):
        self.delete_redis()

        self.client.post(self.authenticate_url, data={"phone_number": self.phone_number})
        validate_response = self.client.post(self.validate_url, data={"phone_number": self.phone_number,
                                                                      "code": self.code})
        registration_token: str = validate_response.data["registration_token"]
        response = self.client.post(self.register_url, data={
            "phone_number": "09112345678",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "registration_token": registration_token,
            "password": self.password
        })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, error_messages.REGISTRATION_TOKEN_IS_NOT_VALID_ERROR_MESSAGE)

    def test_if_register_works(self):
        self.delete_redis()

        self.client.post(self.authenticate_url, data={"phone_number": self.phone_number})
        validate_response = self.client.post(self.validate_url, data={"phone_number": self.phone_number,
                                                                      "code": self.code})
        registration_token: str = validate_response.data["registration_token"]
        response = self.client.post(self.register_url, data={
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "registration_token": registration_token,
            "password": self.password
        })

        self.assertIn("token", response.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsNone(redis_client.registration_token_redis.get(
            key_generators.get_registration_token_key(registration_token)
        ))

        customer_created = Customer.objects.filter(phone_number=self.phone_number).exists()
        self.assertTrue(customer_created)
