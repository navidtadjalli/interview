from django.conf import settings

from achare_interview.utils.redis_utils import key_generators
from achare_interview.utils.redis_utils.redis_client import attempts_redis


def set_attempts(key: str, attempts_count: int):
    attempts_redis.set(key,
                       attempts_count,
                       ex=settings.ATTEMPTS_TIME_TO_LIVE)


def get_attempts(key: str):
    redis_value: bytes = attempts_redis.get(key)
    if not redis_value:
        return 0

    return int(redis_value)


def set_attempts_for_phone_number_for_authenticate(phone_number: str, attempts_count: int):
    set_attempts(key_generators.get_phone_number_attempts_key_for_authenticate(phone_number), attempts_count)


def get_attempts_for_phone_number_for_authenticate(phone_number: str) -> int:
    return get_attempts(key_generators.get_phone_number_attempts_key_for_authenticate(phone_number))


def set_attempts_for_ip_for_authenticate(ip: str, attempts_count: int):
    set_attempts(key_generators.get_ip_attempts_key_for_authenticate(ip), attempts_count)


def get_attempts_for_ip_for_authenticate(ip: str) -> int:
    return get_attempts(key_generators.get_ip_attempts_key_for_authenticate(ip))


def set_attempts_for_phone_number_for_validate(phone_number: str, attempts_count: int):
    set_attempts(key_generators.get_phone_number_attempts_key_for_validate(phone_number), attempts_count)


def set_attempts_for_ip_for_validate(ip: str, attempts_count: int):
    set_attempts(key_generators.get_ip_attempts_key_for_validate(ip), attempts_count)


def get_attempts_for_phone_number_for_validate(phone_number: str):
    return get_attempts(key_generators.get_phone_number_attempts_key_for_validate(phone_number))


def get_attempts_for_ip_for_validate(ip: str):
    return get_attempts(key_generators.get_ip_attempts_key_for_validate(ip))
