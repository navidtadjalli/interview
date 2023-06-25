from http import HTTPStatus
from typing import Optional

from django.urls import reverse

from achare_interview.utils import error_messages
from achare_interview.utils.redis_utils import redis_client, key_generators
from tests.custom_api_test_case import CustomAPITestCase


class AttemptMiddlewareTestCase(CustomAPITestCase):
    def setUp(self):
        self.login_url = reverse("login")
        self.authenticate_url = reverse("authenticate")
        self.validate_url = reverse("validate")

        self.phone_numbers = [f"0912305678{i}" for i in range(1, 5)]
        self.ips = [f"192.168.1.{i}" for i in range(1, 5)]

        self.phone_number_attempts_keys = [key_generators.get_phone_number_attempts_key(pn)
                                           for pn in self.phone_numbers]
        self.ip_attempts_keys = [key_generators.get_ip_attempts_key(ip)
                                 for ip in self.ips]

    def call_authenticate_endpoint(self, phone_number: str, ip: Optional[str] = None):
        response = self.call_endpoint_with_post(self.authenticate_url,
                                                data={
                                                    "phone_number": phone_number
                                                },
                                                headers={
                                                    "X_FORWARDED_FOR": ip
                                                })

        return response

    def test_if_request_attempts_for_phone_number_saves_into_redis(self):
        self.reset_redis()

        self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
        redis_value: bytes = redis_client.attempts_redis.get(self.phone_number_attempts_keys[0])

        self.assertIsNotNone(redis_value)

        redis_value_decoded: str = redis_value.decode(encoding='utf-8')

        self.assertEqual(redis_value_decoded, "1")

    def test_if_request_attempts_for_phone_number_increases_on_request(self):
        self.reset_redis()

        self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
        self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[1])

        redis_value: bytes = redis_client.attempts_redis.get(self.phone_number_attempts_keys[0])
        redis_value_decoded: str = redis_value.decode(encoding='utf-8')

        self.assertEqual(redis_value_decoded, "2")

    def test_if_request_attempts_count_for_phone_number_get_checked(self):
        self.reset_redis()

        self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
        self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[1])
        self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[2])
        response = self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[3])

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, error_messages.IP_HAS_BEEN_BLOCKED_ERROR_MESSAGE)

    def test_if_request_attempts_for_ip_saves_into_redis(self):
        self.reset_redis()

        self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
        redis_value: bytes = redis_client.attempts_redis.get(self.ip_attempts_keys[0])

        self.assertIsNotNone(redis_value)

        redis_value_decoded: str = redis_value.decode(encoding='utf-8')

        self.assertEqual(redis_value_decoded, "1")

    def test_if_request_attempts_for_ip_increases_on_request(self):
        self.reset_redis()

        self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
        self.call_authenticate_endpoint(self.phone_numbers[1], self.ips[0])

        redis_value: bytes = redis_client.attempts_redis.get(self.ip_attempts_keys[0])
        redis_value_decoded: str = redis_value.decode(encoding='utf-8')

        self.assertEqual(redis_value_decoded, "2")

    def test_if_request_attempts_count_for_ip_get_checked(self):
        self.reset_redis()

        self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
        self.call_authenticate_endpoint(self.phone_numbers[1], self.ips[0])
        self.call_authenticate_endpoint(self.phone_numbers[2], self.ips[0])
        response = self.call_authenticate_endpoint(self.phone_numbers[3], self.ips[0])

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, error_messages.IP_HAS_BEEN_BLOCKED_ERROR_MESSAGE)

    # def test_if_different_attempts_from_one_ip_and_different_phone_numbers_gets_checked(self):
    #     self.delete_redis_keys()
    #     fake_code = True
    #
    #     create_validation_code(self.phone_numbers[0], self.ips[0])
    #     create_validation_code(self.phone_numbers[1], self.ips[0])
    #     create_validation_code(self.phone_numbers[2], self.ips[0])
    #
    #     with self.assertRaises(exceptions.MaximumIPAttemptException):
    #         create_validation_code(self.phone_numbers[3], self.ips[0])
    #
    # # postponing remaining tests after middleware created
    # # attempts ttl
    # # def test_if_phone_number_get_blocked_after_three_times(self):
    # # def test_if_ip_get_blocked_after_three_times(self):
    # # def test_if_request_blocked_ips_has_ttl(self):
    # # def test_if_attempts_count_get_deleted_after_successful_validation

    # def test_if_different_attempts_from_different_ips_increases_phone_number_attempts(self):
    #     self.delete_redis_keys()
    #     fake_code = True
    #
    #     create_validation_code(self.phone_numbers[0], self.ips[0])
    #     create_validation_code(self.phone_numbers[0], self.ips[1])
    #     create_validation_code(self.phone_numbers[0], self.ips[2])
    #
    #     with self.assertRaises(exceptions.MaximumPhoneNumberAttemptException):
    #         create_validation_code(self.phone_numbers[0], self.ips[3])
    #
    #
