from django.test import TestCase

from achare_interview.utils import exceptions
from achare_interview.utils.redis_client import validation_code_redis
from achare_interview.utils.validation_code import ValidationCode


class ValidationCodeTestCase(TestCase):
    def setUp(self):
        self.validation_code_instance = ValidationCode()

        self.phone_numbers = [f"0912305678{i}" for i in range(1, 5)]
        self.ips = [f"192.168.1.{i}" for i in range(1, 5)]

        self.code_keys = [f"{pn}_code" for pn in self.phone_numbers]
        self.phone_number_attempts_keys = [f"{pn}_attempts" for pn in self.phone_numbers]
        self.ip_attempts_keys = [f"{ip}_attempts" for ip in self.ips]

    def delete_redis_keys(self):
        for key in self.code_keys + self.phone_number_attempts_keys + self.ip_attempts_keys:
            validation_code_redis.delete(key)

    def test_if_validation_code_has_fake_code_property(self):
        self.assertTrue(hasattr(self.validation_code_instance, 'fake_code'))

    def test_if_validation_code_has_get_validation_code_method(self):
        self.assertTrue(hasattr(self.validation_code_instance, 'get_validation_code'))

    def test_if_get_validation_code_has_phone_number_arg(self):
        with self.assertRaises(TypeError):
            self.validation_code_instance.get_validation_code(ip='')

    def test_if_get_validation_code_has_ip_arg(self):
        with self.assertRaises(TypeError):
            self.validation_code_instance.get_validation_code(phone_number='')

    def test_if_fake_code_works_returns_last_six_character_of_phone_number(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = True

        generated_code: str = self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])

        # Since random code does not start with zero the generated code must start with zero
        self.assertEqual(generated_code[0], "0")
        self.assertEqual(generated_code, self.phone_numbers[0][-6:])

    def test_if_get_validation_code_returns_random_code(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = False

        generated_code: str = self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])

        # Since random code does not start with zero the generated code can not be last 6 number
        self.assertNotEqual(generated_code, self.phone_numbers[0][-6:])

    def test_if_get_validation_code_add_code_to_redis(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        redis_value: bytes = validation_code_redis.get(self.code_keys[0])
        redis_value_str: str = redis_value.decode(encoding='utf-8')

        self.assertIsNotNone(validation_code_redis.get(self.code_keys[0]))
        self.assertEqual(redis_value_str, self.phone_numbers[0][-6:])

    def test_if_added_keys_to_redis_has_ttl(self):
        self.delete_redis_keys()

        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])

        self.assertNotEqual(validation_code_redis.ttl(self.code_keys[0]), -1)

    def test_if_request_attempts_for_phone_number_saves_into_redis(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        redis_value: bytes = validation_code_redis.get(self.phone_number_attempts_keys[0])
        redis_value_decoded: str = redis_value.decode(encoding='utf-8')

        self.assertEqual(redis_value_decoded, "1")

    def test_if_request_attempts_for_phone_number_increases_on_request(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        redis_value: bytes = validation_code_redis.get(self.phone_number_attempts_keys[0])
        redis_value_decoded: str = redis_value.decode(encoding='utf-8')

        self.assertEqual(redis_value_decoded, "2")

    def test_if_request_attempts_count_for_phone_number_get_checked(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])

        with self.assertRaises(exceptions.MaximumPhoneNumberAttemptException):
            self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])

    def test_if_different_attempts_from_different_ips_increases_phone_number_attempts(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[1])
        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[2])

        with self.assertRaises(exceptions.MaximumPhoneNumberAttemptException):
            self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[3])

    def test_if_request_attempts_for_ip_saves_into_redis(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        redis_value: bytes = validation_code_redis.get(self.ip_attempts_keys[0])
        redis_value_decoded: str = redis_value.decode(encoding='utf-8')

        self.assertEqual(redis_value_decoded, "1")

    def test_if_request_attempts_for_ip_increases_on_request(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        redis_value: bytes = validation_code_redis.get(self.ip_attempts_keys[0])
        redis_value_decoded: str = redis_value.decode(encoding='utf-8')

        self.assertEqual(redis_value_decoded, "2")

    def test_if_request_attempts_count_for_ip_get_checked(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        self.validation_code_instance.get_validation_code(self.phone_numbers[1], self.ips[0])

        with self.assertRaises(exceptions.MaximumIPAttemptException):
            self.validation_code_instance.get_validation_code(self.phone_numbers[2], self.ips[0])

    def test_if_different_attempts_from_one_ip_and_different_phone_numbers_gets_checked(self):
        self.delete_redis_keys()
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_numbers[0], self.ips[0])
        self.validation_code_instance.get_validation_code(self.phone_numbers[1], self.ips[0])
        self.validation_code_instance.get_validation_code(self.phone_numbers[2], self.ips[0])

        with self.assertRaises(exceptions.MaximumIPAttemptException):
            self.validation_code_instance.get_validation_code(self.phone_numbers[3], self.ips[0])

    # postponing remaining tests after middleware created
    # def test_if_phone_number_get_blocked_after_three_times(self):
    # def test_if_ip_get_blocked_after_three_times(self):
    # def test_if_request_blocked_ips_has_ttl(self):
    # def test_if_attempts_count_get_deleted_after_successful_validation
