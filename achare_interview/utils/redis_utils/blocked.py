from django.conf import settings

from achare_interview.utils.redis_utils import key_generators
from achare_interview.utils.redis_utils.redis_client import blocked_redis


def set_block_key(key: str):
    blocked_redis.set(key,
                      1,
                      ex=settings.BLOCKED_KEY_TIME_TO_LIVE)


def is_key_blocked(key: str) -> bool:
    redis_value: bytes = blocked_redis.get(key)

    if not redis_value:
        return False

    return int(redis_value) == 1


def set_block_key_for_phone_number(phone_number: str):
    set_block_key(key_generators.get_blocked_key_for_phone_number(phone_number))


def is_phone_number_blocked(phone_number: str) -> bool:
    return is_key_blocked(key_generators.get_blocked_key_for_phone_number(phone_number))


def set_block_key_for_ip(ip: str):
    set_block_key(key_generators.get_blocked_key_for_ip(ip))


def is_ip_blocked(ip: str):
    return is_key_blocked(key_generators.get_blocked_key_for_ip(ip))
