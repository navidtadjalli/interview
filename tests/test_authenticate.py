from http import HTTPStatus

from django.conf import settings
from django.urls import reverse

from achare_interview.utils.redis_utils import redis_client, key_generators
from customer.models import Customer
from tests.custom_api_test_case import CustomAPITestCase


class AuthenticateTestCase(CustomAPITestCase):
    def setUp(self):
        self.url = reverse('authenticate')

    def test_if_authenticate_endpoint_exists(self):
        self.reset_redis()
        self.assertNotEqual(self.call_endpoint_with_get(self.url).status_code, HTTPStatus.NOT_FOUND)

    def test_if_validate_endpoint_method_type_is_post(self):
        self.reset_redis()
        self.assertEqual(self.call_endpoint_with_get(self.url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertNotEqual(self.call_endpoint_with_post(self.url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_if_authenticate_checks_phone_number_is_sent_in_body(self):
        self.reset_redis()
        self.assertEqual(self.call_endpoint_with_post(self.url).status_code, HTTPStatus.BAD_REQUEST)

    def test_if_authenticate_validates_phone_number_being_numeric(self):
        self.reset_redis()
        self.assertEqual(self.call_endpoint_with_post(self.url,
                                                      data={"phone_number": "test"}).status_code,
                         HTTPStatus.BAD_REQUEST)

    def test_if_authenticate_validates_phone_number_length(self):
        self.reset_redis()
        self.assertEqual(self.call_endpoint_with_post(self.url,
                                                      data={"phone_number": "09"}).status_code, HTTPStatus.BAD_REQUEST,
                         msg="Authenticate does not check have minimum length validation for phone_number field")
        self.assertEqual(self.call_endpoint_with_post(self.url,
                                                      data={"phone_number": "09090909090909"}).status_code,
                         HTTPStatus.BAD_REQUEST,
                         msg="Authenticate does not check have maximum length validation for phone_number field")

    def test_if_authenticate_response_contains_duration(self):
        self.reset_redis()
        response = self.call_endpoint_with_post(self.url,
                                                data={"phone_number": "09123456789"})
        self.assertIn("duration", response.data)
        self.assertEqual(response.data["duration"], settings.GENERATED_CODE_TIME_TO_LIVE)

    def test_if_authenticate_create_validation_code_for_user(self):
        self.reset_redis()

        phone_number: str = "09123456789"
        redis_key: str = key_generators.get_code_key(phone_number)

        response = self.call_endpoint_with_post(self.url,
                                                data={"phone_number": phone_number})

        self.assertEqual(response.status_code, HTTPStatus.OK)

        redis_value: bytes = redis_client.validation_code_redis.get(redis_key)
        self.assertIsNotNone(redis_value)

        redis_value_str: str = redis_value.decode(encoding='utf-8')
        self.assertEqual(redis_value_str, phone_number[-6:])

    def test_if_authenticate_responses_contains_can_login_field_if_phone_number_exists(self):
        self.reset_redis()

        phone_number: str = "09123456789"

        customer: Customer = Customer()
        customer.phone_number = phone_number
        customer.set_password('test')
        customer.save()

        response = self.call_endpoint_with_post(self.url,
                                                data={"phone_number": phone_number})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("can_login", response.data)
        self.assertTrue(response.data["can_login"])
