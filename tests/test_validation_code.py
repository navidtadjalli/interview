from django.test import TestCase
from achare_interview.utils.redis_client import validation_code_redis
from achare_interview.utils.validation_code import ValidationCode


class ValidationCodeTestCase(TestCase):
    def setUp(self):
        self.validation_code_instance = ValidationCode()
        self.phone_number = "09123056789"

    def test_if_validation_code_has_fake_code_property(self):
        self.assertTrue(hasattr(self.validation_code_instance, 'fake_code'))

    def test_if_validation_code_has_get_validation_code_method(self):
        self.assertTrue(hasattr(self.validation_code_instance, 'get_validation_code'))

    def test_if_get_validation_code_has_phone_number_arg(self):
        with self.assertRaises(TypeError):
            self.validation_code_instance.get_validation_code()

    def test_if_fake_code_works_returns_last_six_character_of_phone_number(self):
        self.validation_code_instance.fake_code = True

        generated_code: str = self.validation_code_instance.get_validation_code(self.phone_number)

        # Since random code does not start with zero the generated code must start with zero
        self.assertEqual(generated_code[0], "0")
        self.assertEqual(generated_code, self.phone_number[-6:])

    def test_if_get_validation_code_returns_random_code(self):
        self.validation_code_instance.fake_code = False

        generated_code: str = self.validation_code_instance.get_validation_code(self.phone_number)

        # Since random code does not start with zero the generated code can not be last 6 number
        self.assertNotEqual(generated_code, self.phone_number[-6:])

    def test_if_get_validation_code_add_code_to_redis(self):
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_number)

        self.assertIsNotNone(validation_code_redis.get(self.phone_number))

    def test_if_added_keys_to_redis_has_ttl(self):
        self.validation_code_instance.fake_code = True

        self.validation_code_instance.get_validation_code(self.phone_number)

        self.assertNotEqual(validation_code_redis.ttl(self.phone_number), -1)

    # expire time for code
    # block after 3
