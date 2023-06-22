from django.test import TestCase

from customer.models import Customer


class CustomerModelFieldsTestCase(TestCase):
    def setUp(self):
        pass

    def test_if_customer_model_has_required_fields(self):
        customer = Customer()

        self.assertTrue(hasattr(customer, "first_name"))
        self.assertTrue(hasattr(customer, "last_name"))
        self.assertTrue(hasattr(customer, "phone_number"))
        self.assertTrue(hasattr(customer, "email"))

    def test_if_registered_at_get_filled_on_creation(self):
        customer = Customer.objects.create(
            first_name="Tony",
            last_name="Stark",
            phone_number="09123456789",
            email="test@test.com"
        )

        self.assertIsNotNone(customer.registered_at)

    def test_if_str_function_of_model_works_properly(self):
        customer = Customer.objects.create(
            first_name="Tony",
            last_name="Stark",
            phone_number="09123456789",
            email="test@test.com"
        )

        self.assertEqual(str(customer), "Stark, Tony")
