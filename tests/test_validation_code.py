from django.conf import settings
from django.test import TestCase

from achare_interview.utils import exceptions
from achare_interview.utils.redis_client import validation_code_redis, reset_redis
from achare_interview.utils.validation_code import create_validation_code


class ValidationCodeTestCase(TestCase):
    def setUp(self):
        self.phone_numbers = [f"0912305678{i}" for i in range(1, 5)]
        self.ips = [f"192.168.1.{i}" for i in range(1, 5)]

        self.code_keys = [f"{pn}_code" for pn in self.phone_numbers]
        self.phone_number_attempts_keys = [f"{pn}_attempts" for pn in self.phone_numbers]
        self.ip_attempts_keys = [f"{ip}_attempts" for ip in self.ips]

    def delete_redis_keys(self):
        reset_redis(validation_code_redis)

    def test_if_get_validation_code_has_phone_number_arg(self):
        with self.assertRaises(TypeError):
            create_validation_code(ip='')

    def test_if_get_validation_code_has_ip_arg(self):
        with self.assertRaises(TypeError):
            create_validation_code(phone_number='')

    def test_if_fake_code_works_returns_last_six_character_of_phone_number(self):
        self.delete_redis_keys()
        fake_code = True

        create_validation_code(self.phone_numbers[0], self.ips[0])
        redis_value: bytes = validation_code_redis.get(self.code_keys[0])
        generated_code: str = redis_value.decode(encoding='utf-8')

        # Since random code does not start with zero the generated code must start with zero
        self.assertEqual(generated_code[0], "0")
        self.assertEqual(generated_code, self.phone_numbers[0][-6:])

    def test_if_get_validation_code_returns_random_code(self):
        self.delete_redis_keys()
        settings.GENERATE_FAKE_CODE = False

        create_validation_code(self.phone_numbers[0], self.ips[0])
        redis_value: bytes = validation_code_redis.get(self.code_keys[0])
        generated_code: str = redis_value.decode(encoding='utf-8')

        # Since random code does not start with zero the generated code can not be last 6 number
        self.assertNotEqual(generated_code, self.phone_numbers[0][-6:])

    def test_if_get_validation_code_add_code_to_redis(self):
        self.delete_redis_keys()
        settings.GENERATE_FAKE_CODE = True

        create_validation_code(self.phone_numbers[0], self.ips[0])
        redis_value: bytes = validation_code_redis.get(self.code_keys[0])
        redis_value_str: str = redis_value.decode(encoding='utf-8')

        self.assertIsNotNone(validation_code_redis.get(self.code_keys[0]))
        self.assertEqual(redis_value_str, self.phone_numbers[0][-6:])

    def test_if_added_keys_to_redis_has_ttl(self):
        self.delete_redis_keys()

        create_validation_code(self.phone_numbers[0], self.ips[0])

        self.assertNotEqual(validation_code_redis.ttl(self.code_keys[0]), -1)
