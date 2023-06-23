from time import sleep

from django.conf import settings
from django.test import TestCase

from achare_interview.utils.redis_client import validation_code_redis, reset_redis, RedisKeyGenerator
from achare_interview.utils.validation_code import create_validation_code


class ValidationCodeTestCase(TestCase):
    def setUp(self):
        self.phone_number = "09123056789"
        self.code_key = RedisKeyGenerator.get_code_key(self.phone_number)

    def delete_redis_keys(self):
        reset_redis(validation_code_redis)

    def test_if_get_validation_code_has_phone_number_arg(self):
        with self.assertRaises(TypeError):
            create_validation_code()

    def test_if_fake_code_works_returns_last_six_character_of_phone_number(self):
        self.delete_redis_keys()
        settings.GENERATE_FAKE_CODE = True

        create_validation_code(self.phone_number)
        redis_value: bytes = validation_code_redis.get(self.code_key)
        generated_code: str = redis_value.decode(encoding='utf-8')

        # Since random code does not start with zero the generated code must start with zero
        self.assertEqual(generated_code[0], "0")
        self.assertEqual(generated_code, self.phone_number[-6:])

    def test_if_get_validation_code_returns_random_code(self):
        self.delete_redis_keys()
        settings.GENERATE_FAKE_CODE = False

        create_validation_code(self.phone_number)
        redis_value: bytes = validation_code_redis.get(self.code_key)
        generated_code: str = redis_value.decode(encoding='utf-8')

        # Since random code does not start with zero the generated code can not be last 6 number
        self.assertNotEqual(generated_code, self.phone_number[-6:])

    def test_if_get_validation_code_add_code_to_redis(self):
        self.delete_redis_keys()
        settings.GENERATE_FAKE_CODE = True

        create_validation_code(self.phone_number)
        redis_value: bytes = validation_code_redis.get(self.code_key)
        redis_value_str: str = redis_value.decode(encoding='utf-8')

        self.assertIsNotNone(validation_code_redis.get(self.code_key))
        self.assertEqual(redis_value_str, self.phone_number[-6:])

    def test_if_added_keys_to_redis_has_ttl(self):
        self.delete_redis_keys()

        create_validation_code(self.phone_number)

        self.assertNotEqual(validation_code_redis.ttl(self.code_key), -1)

    def test_if_added_key_for_code_get_expired(self):
        self.delete_redis_keys()
        settings.GENERATED_CODE_TIME_TO_LIVE = 3
        create_validation_code(self.phone_number)
        sleep(4)

        self.assertIsNone(validation_code_redis.get(self.code_key))
