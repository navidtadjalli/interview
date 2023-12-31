from http import HTTPStatus
from time import sleep

from django.conf import settings
from django.urls import reverse

from achare_interview.utils import error_messages
from tests.custom_api_test_case import CustomAPITestCase


class ValidateTestCase(CustomAPITestCase):
    def setUp(self):
        self.authenticate_url = reverse('authenticate')
        self.url = reverse('validate')

    def test_if_validate_endpoint_exists(self):
        self.reset_redis()
        self.assertNotEqual(self.call_endpoint_with_get(self.url).status_code, HTTPStatus.NOT_FOUND)

    def test_if_validate_endpoint_method_type_is_post(self):
        self.reset_redis()
        self.assertEqual(self.call_endpoint_with_get(self.url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertNotEqual(self.call_endpoint_with_post(self.url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_if_validate_checks_phone_number_and_code_are_sent_in_body(self):
        self.reset_redis()
        response = self.call_endpoint_with_post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("phone_number", response.data.keys())
        self.assertIn("code", response.data.keys())

    # skipping phone_number tests because it got tested in test_authenticate test cases it'll be skipped here

    def test_if_validate_validates_code_being_numeric(self):
        self.reset_redis()
        self.assertEqual(self.call_endpoint_with_post(self.url,
                                                      data={
                                                          "phone_number": "09123456789",
                                                          "code": "test"
                                                      }).status_code, HTTPStatus.BAD_REQUEST)

    def test_if_validate_validates_phone_number_length(self):
        self.reset_redis()
        self.assertEqual(self.call_endpoint_with_post(self.url,
                                                      data={
                                                          "phone_number": "09123456789",
                                                          "code": "123"
                                                      }).status_code, HTTPStatus.BAD_REQUEST,
                         msg="Validate does not check have minimum length validation for code field")
        self.assertEqual(self.call_endpoint_with_post(self.url,
                                                      data={
                                                          "phone_number": "09123456789",
                                                          "code": "1234567"
                                                      }).status_code, HTTPStatus.BAD_REQUEST,
                         msg="Validate does not check have maximum length validation for code field")

    def test_if_validate_checks_code(self):
        self.reset_redis()

        phone_number: str = "09123456789"

        self.call_endpoint_with_post(self.authenticate_url,
                                     data={"phone_number": phone_number})
        response = self.call_endpoint_with_post(self.url,
                                                data={
                                                    "phone_number": phone_number,
                                                    "code": "123456"
                                                })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, error_messages.VALIDATION_CODE_DOES_NOT_MATCH_ERROR_MESSAGE)

    def test_if_validate_gets_a_token_for_registration(self):
        self.reset_redis()

        phone_number: str = "09123456789"

        self.call_endpoint_with_post(self.authenticate_url,
                                     data={"phone_number": phone_number})
        response = self.call_endpoint_with_post(self.url,
                                                data={
                                                    "phone_number": phone_number,
                                                    "code": "456789"
                                                })

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("registration_token", response.data)

    def test_validate_responses_for_expired_code(self):
        self.reset_redis()
        settings.GENERATED_CODE_TIME_TO_LIVE = 1

        phone_number: str = "09123456789"

        self.call_endpoint_with_post(self.authenticate_url,
                                     data={"phone_number": phone_number})
        sleep(2)
        response = self.call_endpoint_with_post(self.url,
                                                data={"phone_number": phone_number, "code": "456789"})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, error_messages.VALIDATION_CODE_EXPIRED_ERROR_MESSAGE)
