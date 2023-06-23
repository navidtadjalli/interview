import random
from typing import Optional

from django.conf import settings

from achare_interview.utils import exceptions
from achare_interview.utils.redis_client import validation_code_redis, RedisKeyGenerator


def generate_validation_code(phone_number: str) -> str:
    if settings.GENERATE_FAKE_CODE:
        return phone_number[-6:]

    return random.choice("123456789") + ''.join(random.choices("01234567890", k=5))


def get_attempts(key: str) -> int:
    redis_value: Optional[bytes] = validation_code_redis.get(key)
    attempt: int = 0
    if redis_value:
        attempt = int(redis_value)

    return attempt


def add_code_to_redis(phone_number: str, code: str):
    validation_code_redis.set(RedisKeyGenerator.get_code_key(phone_number),
                              code,
                              ex=settings.GENERATED_CODE_TIME_TO_LIVE)


def add_phone_number_attempts_to_redis(phone_number: str, phone_number_attempts: int):
    validation_code_redis.set(RedisKeyGenerator.get_phone_number_attempts_key(phone_number),
                              phone_number_attempts + 1)


def add_ip_attempts_to_redis(ip: str, ip_attempts: int):
    validation_code_redis.set(RedisKeyGenerator.get_phone_number_attempts_key(ip),
                              ip_attempts + 1)


def check_phone_number_attempts(phone_number_attempts: int):
    if phone_number_attempts >= settings.MAXIMUM_CODE_REQUEST_COUNT:
        raise exceptions.MaximumPhoneNumberAttemptException()


def check_ip_attempts(ip_attempts: int):
    if ip_attempts >= settings.MAXIMUM_CODE_REQUEST_COUNT:
        raise exceptions.MaximumIPAttemptException()


def create_validation_code(phone_number: str, ip: str):
    phone_number_attempts: int = get_attempts(RedisKeyGenerator.get_phone_number_attempts_key(phone_number))
    ip_attempts: int = get_attempts(RedisKeyGenerator.get_ip_attempts_key(ip))

    check_phone_number_attempts(phone_number_attempts)
    check_ip_attempts(ip_attempts)

    generated_code: str = generate_validation_code(phone_number)
    add_code_to_redis(phone_number, generated_code)
    add_phone_number_attempts_to_redis(phone_number, phone_number_attempts)
    add_ip_attempts_to_redis(ip, ip_attempts)
