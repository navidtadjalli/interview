from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APITestCase

from achare_interview.utils import error_messages
from customer.models import Customer
from tests.custom_api_test_case import CustomAPITestCase


class LoginTestCase(CustomAPITestCase):
    def setUp(self):
        self.authenticate_url = reverse('authenticate')
        self.validate_url = reverse('validate')
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        self.phone_number = "09123456789"
        self.code = self.phone_number[-6:]
        self.first_name = "first_name"
        self.last_name = "last_name"
        self.password = "password"

    def test_if_login_endpoint_exists(self):
        self.reset_redis()
        self.assertNotEqual(self.call_endpoint_with_get(self.login_url).status_code, HTTPStatus.NOT_FOUND)

    def test_if_login_endpoint_method_type_is_post(self):
        self.reset_redis()

        self.assertEqual(self.call_endpoint_with_get(self.login_url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertNotEqual(self.call_endpoint_with_post(self.login_url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_if_login_checks_required_fields_are_sent_in_body(self):
        self.reset_redis()
        response = self.call_endpoint_with_post(self.login_url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("phone_number", response.data.keys())
        self.assertIn("password", response.data.keys())

    # skipping phone_number tests because it got tested in test_authenticate test cases it'll be skipped here

    def test_if_login_requires_password(self):
        self.reset_redis()
        response = self.call_endpoint_with_post(self.login_url,
                                                data={
                                                    "phone_number": self.phone_number
                                                })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_if_login_checks_phone_number_existence(self):
        self.reset_redis()

        response = self.call_endpoint_with_post(self.login_url,
                                                data={
                                                    "phone_number": self.phone_number,
                                                    "password": self.password + "test"
                                                })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, error_messages.PHONE_NUMBER_OR_PASSWORD_IS_INCORRECT_ERROR_MESSAGE)

    def test_if_login_checks_password(self):
        self.reset_redis()

        customer: Customer = Customer.objects.create_user(
            phone_number=self.phone_number
        )
        customer.set_password(self.password)
        customer.save()

        response = self.call_endpoint_with_post(self.login_url,
                                                data={
                                                    "phone_number": self.phone_number,
                                                    "password": self.password + "test"
                                                })

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, error_messages.PHONE_NUMBER_OR_PASSWORD_IS_INCORRECT_ERROR_MESSAGE)

    def test_if_login_works(self):
        self.reset_redis()

        customer: Customer = Customer.objects.create_user(
            phone_number=self.phone_number
        )
        customer.set_password(self.password)
        customer.save()

        response = self.call_endpoint_with_post(self.login_url,
                                                data={
                                                    "phone_number": self.phone_number,
                                                    "password": self.password
                                                })

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("token", response.data)

    def test_if_user_can_login_after_registered(self):
        self.reset_redis()

        self.call_endpoint_with_post(self.authenticate_url,
                                     data={"phone_number": self.phone_number})
        validate_response = self.call_endpoint_with_post(self.validate_url,
                                                         data={
                                                             "phone_number": self.phone_number,
                                                             "code": self.code
                                                         })
        registration_token: str = validate_response.data["registration_token"]
        self.call_endpoint_with_post(self.register_url,
                                     data={
                                         "phone_number": self.phone_number,
                                         "first_name": self.first_name,
                                         "last_name": self.last_name,
                                         "registration_token": registration_token,
                                         "password": self.password
                                     })
        response = self.call_endpoint_with_post(self.login_url,
                                                data={
                                                    "phone_number": self.phone_number,
                                                    "password": self.password
                                                })

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("token", response.data)
