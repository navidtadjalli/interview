from http import HTTPStatus
from typing import Optional

from django.conf import settings
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

    # def call_authenticate_endpoint(self, phone_number: str, ip: Optional[str] = None):
    #     response = self.call_endpoint_with_post(self.authenticate_url,
    #                                             data={
    #                                                 "phone_number": phone_number
    #                                             },
    #                                             headers={
    #                                                 "X_FORWARDED_FOR": ip
    #                                             })
    #
    #     return response
    #
    # def call_validate_endpoint(self, phone_number: str, ip: str, code: str):
    #     return self.call_endpoint_with_post(
    #         self.validate_url,
    #         data={"phone_number": phone_number, "code": code},
    #         headers={"X_FORWARDED_FOR": ip}
    #     )
    #
    # def call_login_endpoint(self, phone_number: str, ip: str):
    #     return self.call_endpoint_with_post(
    #         self.login_url,
    #         data={"phone_number": phone_number, "password": "password"},
    #         headers={"X_FORWARDED_FOR": ip}
    #     )
    #
    # def test_if_authenticate_attempts_for_phone_number_saves_into_redis(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     phone_number_attempts_redis_value: bytes = redis_client.attempts_redis.get(self.phone_number_attempts_keys[0])
    #     ip_attempts_redis_value: bytes = redis_client.attempts_redis.get(self.ip_attempts_keys[0])
    #
    #     self.assertIsNotNone(phone_number_attempts_redis_value)
    #     self.assertIsNotNone(ip_attempts_redis_value)
    #
    #     phone_number_attempts: str = phone_number_attempts_redis_value.decode(encoding='utf-8')
    #     ip_attempts: str = ip_attempts_redis_value.decode(encoding='utf-8')
    #
    #     self.assertEqual(phone_number_attempts, "1", msg="Phone number attempts did not saved into redis")
    #     self.assertEqual(ip_attempts, "1", msg="IP attempts did not saved into redis")
    #
    # def test_if_saved_authenticate_attempts_for_phone_number_and_ip_have_ttl_in_redis(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     phone_number_attempts_ttl: bytes = redis_client.attempts_redis.ttl(self.phone_number_attempts_keys[0])
    #     ip_attempts_ttl: bytes = redis_client.attempts_redis.ttl(self.ip_attempts_keys[0])
    #
    #     self.assertNotEqual(phone_number_attempts_ttl, -1, msg="Phone number attempts do not have TTL")
    #     self.assertNotEqual(ip_attempts_ttl, -1, msg="IP attempts do not have TTL")
    #
    # def test_if_authenticate_attempts_for_phone_number_and_ip_increases_on_request(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #
    #     phone_number_attempts_redis_value: bytes = redis_client.attempts_redis.get(self.phone_number_attempts_keys[0])
    #     phone_number_attempts: str = phone_number_attempts_redis_value.decode(encoding='utf-8')
    #
    #     ip_attempts_redis_value: bytes = redis_client.attempts_redis.get(self.ip_attempts_keys[0])
    #     ip_attempts: str = ip_attempts_redis_value.decode(encoding='utf-8')
    #
    #     self.assertEqual(phone_number_attempts, "2", msg="Phone number attempts did not get increased")
    #     self.assertEqual(ip_attempts, "2", msg="IP attempts did not get increased")
    #
    # def test_if_authenticate_attempts_count_for_phone_number_get_checked(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[1])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[2])
    #     response = self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[3])
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
    #     self.assertEqual(response.data, error_messages.REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE)
    #
    # def test_if_authenticate_attempts_count_for_ip_get_checked(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[1], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[2], self.ips[0])
    #     response = self.call_authenticate_endpoint(self.phone_numbers[3], self.ips[0])
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
    #     self.assertEqual(response.data, error_messages.REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE)
    #
    # def test_if_authenticate_phone_number_blocked_key_is_added_to_redis(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[1])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[2])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[3])
    #
    #     redis_value: bytes = redis_client.blocked_redis.get(key_generators.get_blocked_key_for_phone_number(
    #         self.phone_numbers[0]))
    #
    #     self.assertIsNotNone(redis_value)
    #
    #     blocked_value: int = int(redis_value)
    #     self.assertEqual(blocked_value, 1)
    #
    # def test_if_authenticate_phone_number_blocked_key_has_ttl(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[1])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[2])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[3])
    #
    #     ttl: int = redis_client.blocked_redis.ttl(key_generators.get_blocked_key_for_phone_number(
    #         self.phone_numbers[0]))
    #
    #     self.assertNotEqual(ttl, -1)
    #     self.assertEqual(ttl, settings.BLOCKED_KEY_TIME_TO_LIVE)
    #
    # def test_if_authenticate_phone_number_get_blocked_after_three_times(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[1])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[2])
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[3])
    #
    #     response = self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[3])
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
    #     self.assertEqual(response.data, error_messages.PHONE_NUMBER_HAS_BEEN_BLOCKED_ERROR_MESSAGE)
    #
    # def test_if_authenticate_ip_blocked_key_is_added_to_redis(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[1], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[2], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[3], self.ips[0])
    #
    #     redis_value: bytes = redis_client.blocked_redis.get(key_generators.get_blocked_key_for_ip(
    #         self.ips[0]))
    #
    #     self.assertIsNotNone(redis_value)
    #
    #     blocked_value: int = int(redis_value)
    #     self.assertEqual(blocked_value, 1)
    #
    # def test_if_authenticate_ip_blocked_key_has_ttl(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[1], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[2], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[3], self.ips[0])
    #
    #     ttl: int = redis_client.blocked_redis.ttl(key_generators.get_blocked_key_for_ip(
    #         self.ips[0]))
    #
    #     self.assertNotEqual(ttl, -1)
    #     self.assertEqual(ttl, settings.BLOCKED_KEY_TIME_TO_LIVE)
    #
    # def test_if_authenticate_ip_get_blocked_after_three_times(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[1], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[2], self.ips[0])
    #     self.call_authenticate_endpoint(self.phone_numbers[3], self.ips[0])
    #
    #     response = self.call_authenticate_endpoint(self.phone_numbers[3], self.ips[0])
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
    #     self.assertEqual(response.data, error_messages.IP_HAS_BEEN_BLOCKED_ERROR_MESSAGE)

    # def test_if_invalid_code_leads_to_blocking_after_3_tries(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #
    #     response = None
    #     for i in range(0, 3):
    #         response = self.call_validate_endpoint(self.phone_numbers[0], self.ips[i], "111111")
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN,
    #                      msg="Validate endpoint status is not forbidden after 3 times.")
    #     self.assertEqual(response.data, error_messages.REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE,
    #                      msg="Validate endpoint content is not equal to REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE "
    #                          "after 3 times.")
    #
    #     response = self.call_validate_endpoint(self.phone_numbers[0], self.ips[3], "111111")
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN,
    #                      msg="Validate endpoint status is not forbidden after being called for more than 3 times.")
    #     self.assertEqual(response.data, error_messages.PHONE_NUMBER_HAS_BEEN_BLOCKED_ERROR_MESSAGE,
    #                      msg="Validate endpoint content is not equal to PHONE_NUMBER_HAS_BEEN_BLOCKED_ERROR_MESSAGE "
    #                          "after being called for more than 3 times.")
    #
    # def test_if_blocking_ip_works_for_validate_endpoint(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #
    #     response = None
    #     for i in range(0, 3):
    #         response = self.call_validate_endpoint(self.phone_numbers[i], self.ips[0])
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN,
    #                      msg="Validate endpoint status is not forbidden after 3 times.")
    #     self.assertEqual(response.data, error_messages.REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE,
    #                      msg="Validate endpoint content is not equal to REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE "
    #                          "after 3 times.")
    #
    #     response = self.call_validate_endpoint(self.phone_numbers[3], self.ips[0])
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN,
    #                      msg="Validate endpoint status is not forbidden after being called for more than 3 times.")
    #     self.assertEqual(response.data, error_messages.IP_HAS_BEEN_BLOCKED_ERROR_MESSAGE,
    #                      msg="Validate endpoint content is not equal to IP_HAS_BEEN_BLOCKED_ERROR_MESSAGE "
    #                          "after being called for more than 3 times.")
    #
    #
    # def test_if_phone_number_attempts_count_get_deleted_after_successful_validation(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #     self.call_endpoint_with_post(self.validate_url,
    #                                  data={
    #                                      "phone_number": self.phone_numbers[0],
    #                                      "code": self.phone_numbers[0][-6:]
    #                                  })
    #
    #     redis_value: bytes = redis_client.attempts_redis.get(key_generators.get_phone_number_attempts_key(
    #         self.phone_numbers[0]))
    #
    #     self.assertIsNone(redis_value)
    #
    # def test_if_blocking_phone_number_works_for_login_endpoint(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #
    #     response = None
    #     for i in range(0, 3):
    #         response = self.call_login_endpoint(self.phone_numbers[0], self.ips[i])
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN,
    #                      msg="Login endpoint status is not forbidden after 3 times.")
    #     self.assertEqual(response.data, error_messages.REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE,
    #                      msg="Login endpoint content is not equal to REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE "
    #                          "after 3 times.")
    #
    #     response = self.call_login_endpoint(self.phone_numbers[0], self.ips[3])
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN,
    #                      msg="Login endpoint status is not forbidden after being called for more than 3 times.")
    #     self.assertEqual(response.data, error_messages.PHONE_NUMBER_HAS_BEEN_BLOCKED_ERROR_MESSAGE,
    #                      msg="Login endpoint content is not equal to PHONE_NUMBER_HAS_BEEN_BLOCKED_ERROR_MESSAGE "
    #                          "after being called for more than 3 times.")
    #
    # def test_if_blocking_ip_works_for_login_endpoint(self):
    #     self.reset_redis()
    #
    #     self.call_authenticate_endpoint(self.phone_numbers[0], self.ips[0])
    #
    #     response = None
    #     for i in range(0, 3):
    #         response = self.call_login_endpoint(self.phone_numbers[i], self.ips[0])
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN,
    #                      msg="Login endpoint status is not forbidden after 3 times.")
    #     self.assertEqual(response.data, error_messages.REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE,
    #                      msg="Login endpoint content is not equal to REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE "
    #                          "after 3 times.")
    #
    #     response = self.call_login_endpoint(self.phone_numbers[3], self.ips[0])
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN,
    #                      msg="Login endpoint status is not forbidden after being called for more than 3 times.")
    #     self.assertEqual(response.data, error_messages.IP_HAS_BEEN_BLOCKED_ERROR_MESSAGE,
    #                      msg="Login endpoint content is not equal to IP_HAS_BEEN_BLOCKED_ERROR_MESSAGE "
    #                          "after being called for more than 3 times.")
    #
    # def test_if_attempts_count_get_deleted_after_successful_login(self):
