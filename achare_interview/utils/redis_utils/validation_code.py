import random

from django.conf import settings

from achare_interview.utils import exceptions
from achare_interview.utils.redis_utils import redis_client, key_generators


def generate_validation_code(phone_number: str) -> str:
    if settings.GENERATE_FAKE_CODE:
        return phone_number[-6:]

    return random.choice("123456789") + ''.join(random.choices("01234567890", k=5))


def add_code_to_redis(phone_number: str, code: str):
    redis_client.validation_code_redis.set(key_generators.get_code_key(phone_number),
                                           code,
                                           ex=settings.GENERATED_CODE_TIME_TO_LIVE)


def get_code_from_redis(phone_number: str) -> str:
    redis_value: bytes = redis_client.validation_code_redis.get(key_generators.get_code_key(phone_number))
    if not redis_value:
        raise exceptions.ValidationCodeExpiredException()

    return redis_value.decode(encoding="utf-8")


def delete_code_from_redis(phone_number: str):
    redis_client.validation_code_redis.delete(key_generators.get_code_key(phone_number))


def create_validation_code(phone_number: str):
    generated_code: str = generate_validation_code(phone_number)
    add_code_to_redis(phone_number, generated_code)


def validate_validation_code(phone_number: str, code: str):
    redis_code: str = get_code_from_redis(phone_number)

    if code != redis_code:
        raise exceptions.ValidationCodeDoesNotMatchException()

    delete_code_from_redis(phone_number)
