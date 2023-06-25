from django.conf import settings

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


def delete_attempts(key: str):
    attempts_redis.delete(key)
