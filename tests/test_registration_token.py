from achare_interview.utils.redis_utils import redis_client, key_generators
from achare_interview.utils.redis_utils.registration_token import get_registration_token
from tests.custom_api_test_case import CustomAPITestCase


class ValidationCodeTestCase(CustomAPITestCase):
    def setUp(self):
        self.phone_number = "09123056789"
        self.phone_number_2 = "09123056780"

    def test_if_get_registration_token_has_phone_number_arg(self):
        with self.assertRaises(TypeError):
            get_registration_token()

    def test_if_get_registration_token_returns_anything(self):
        self.reset_redis()

        self.assertIsNotNone(get_registration_token(self.phone_number))

    def test_if_get_registration_token_returns_random_uuids(self):
        self.reset_redis()

        res1: str = get_registration_token(self.phone_number)
        res2: str = get_registration_token(self.phone_number_2)

        self.assertNotEqual(res1, res2)

    def test_if_get_registration_token_add_token_to_redis(self):
        self.reset_redis()

        token: str = get_registration_token(self.phone_number)
        redis_value: bytes = redis_client.registration_token_redis.get(key_generators.get_registration_token_key(token))

        self.assertIsNotNone(redis_value)

    def test_if_added_token_has_ttl_in_redis(self):
        self.reset_redis()

        token: str = get_registration_token(self.phone_number)
        ttl: int = redis_client.registration_token_redis.ttl(key_generators.get_registration_token_key(token))

        self.assertNotEqual(ttl, -1)

    def test_if_get_registration_token_put_phone_number_as_token_value(self):
        self.reset_redis()

        token: str = get_registration_token(self.phone_number)
        value: bytes = redis_client.registration_token_redis.get(key_generators.get_registration_token_key(token))

        self.assertIsNotNone(value)

        value_str: str = value.decode(encoding="utf-8")

        self.assertEqual(value_str, self.phone_number)
