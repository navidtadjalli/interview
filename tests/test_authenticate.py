from http import HTTPStatus

from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase

from achare_interview.utils.redis_client import validation_code_redis, reset_redis, RedisKeyGenerator
from customer.models import Customer


class AuthenticateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('authenticate')

    def test_if_authenticate_endpoint_exists(self):
        self.assertNotEqual(self.client.post(self.url).status_code, HTTPStatus.NOT_FOUND)

    def test_if_authenticate_checks_phone_number_is_sent_in_body(self):
        self.assertEqual(self.client.post(self.url).status_code, HTTPStatus.BAD_REQUEST)

    def test_if_authenticate_validates_phone_number_being_numeric(self):
        self.assertEqual(self.client.post(self.url,
                                          data={"phone_number": "test"}).status_code, HTTPStatus.BAD_REQUEST)

    def test_if_authenticate_validates_phone_number_length(self):
        self.assertEqual(self.client.post(self.url,
                                          data={"phone_number": "09"}).status_code, HTTPStatus.BAD_REQUEST,
                         msg="Authenticate does not check have minimum length validation for phone_number field")
        self.assertEqual(self.client.post(self.url,
                                          data={"phone_number": "09090909090909"}).status_code, HTTPStatus.BAD_REQUEST,
                         msg="Authenticate does not check have maximum length validation for phone_number field")

    def test_if_authenticate_response_contains_duration(self):
        response = self.client.post(self.url, data={"phone_number": "09123456789"})
        self.assertIn("duration", response.data)
        self.assertEqual(response.data["duration"], settings.GENERATED_CODE_TIME_TO_LIVE)

    def test_if_authenticate_create_validation_code_for_user(self):
        reset_redis(validation_code_redis)

        phone_number: str = "09123456789"
        redis_key: str = RedisKeyGenerator.get_code_key(phone_number)

        response = self.client.post(self.url, data={"phone_number": phone_number})

        self.assertEqual(response.status_code, HTTPStatus.OK)

        redis_value: bytes = validation_code_redis.get(redis_key)
        self.assertIsNotNone(redis_value)

        redis_value_str: str = redis_value.decode(encoding='utf-8')
        self.assertEqual(redis_value_str, phone_number[-6:])

    def test_if_authenticate_checks_phone_number_existence(self):
        reset_redis(validation_code_redis)

        phone_number: str = "09123456789"

        customer: Customer = Customer()
        customer.phone_number = phone_number
        customer.set_password('test')
        customer.save()

        response = self.client.post(self.url, data={"phone_number": phone_number})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
