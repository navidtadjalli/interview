from achare_interview.utils.redis_utils import key_generators
from achare_interview.utils.redis_utils.redis_client import attempts_redis


def set_attempts_for_phone_number(phone_number: str, attempts_count: int):
    attempts_redis.set(key_generators.get_phone_number_attempts_key(phone_number),
                       attempts_count)


def get_attempts_for_phone_number(phone_number: str) -> int:
    redis_value: bytes = attempts_redis.get(key_generators.get_phone_number_attempts_key(phone_number))
    if not redis_value:
        return 0

    return int(redis_value)


def set_attempts_for_ip(ip: str, attempts_count: int):
    attempts_redis.set(key_generators.get_ip_attempts_key(ip),
                       attempts_count)


def get_attempts_for_ip(ip: str) -> int:
    redis_value: bytes = attempts_redis.get(key_generators.get_ip_attempts_key(ip))
    if not redis_value:
        return 0

    return int(redis_value)
