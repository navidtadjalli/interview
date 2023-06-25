from django.conf import settings

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

