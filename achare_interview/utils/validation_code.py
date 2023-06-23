import random
from typing import Optional

from django.conf import settings

from achare_interview.utils import exceptions
from achare_interview.utils.redis_client import validation_code_redis, RedisKeyGenerator


def generate_validation_code(phone_number: str) -> str:
    if settings.GENERATE_FAKE_CODE:
        return phone_number[-6:]

    return random.choice("123456789") + ''.join(random.choices("01234567890", k=5))


def add_code_to_redis(phone_number: str, code: str):
    validation_code_redis.set(RedisKeyGenerator.get_code_key(phone_number),
                              code,
                              ex=settings.GENERATED_CODE_TIME_TO_LIVE)


def create_validation_code(phone_number: str):
    generated_code: str = generate_validation_code(phone_number)
    add_code_to_redis(phone_number, generated_code)


def validate_validation_code(phone_number: str, code: str):
    pass
