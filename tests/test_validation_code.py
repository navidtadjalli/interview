from django.test import TestCase
from achare_interview.utils.validation_code import ValidationCode


class ValidationCodeTestCase(TestCase):
    def setUp(self):
        self.validation_code_instance = ValidationCode()

    def test_if_validation_code_has_fake_code_property(self):
        self.assertTrue(hasattr(self.validation_code_instance, 'fake_code'))

    def test_if_validation_code_has_get_validation_code_method(self):
        self.assertTrue(hasattr(self.validation_code_instance, 'get_validation_code'))

    def test_if_get_validation_code_has_phone_number_arg(self):
        with self.assertRaises(TypeError):
            self.validation_code_instance.get_validation_code()

    def test_if_fake_code_works_returns_last_six_character_of_phone_number(self):
        self.validation_code_instance.fake_code = True

        phone_number: str = "09123456789"
        generated_code: str = self.validation_code_instance.get_validation_code(phone_number)

        self.assertEqual(generated_code, phone_number[-6:])

    def test_if_get_validation_code_returns_random_code(self):
        self.validation_code_instance.fake_code = False

        phone_number: str = "09123056789"
        generated_code: str = self.validation_code_instance.get_validation_code(phone_number)

        # Since random code does not start with zero the generated code can not be last 6 number
        self.assertNotEqual(generated_code, phone_number[-6:])

