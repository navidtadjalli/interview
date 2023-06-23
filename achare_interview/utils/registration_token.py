from uuid import uuid4

from django.conf import settings

from achare_interview.utils.redis_client import registration_token_redis, RedisKeyGenerator


def generate_registration_token() -> str:
    token: str = uuid4().hex
    return token


def add_token_to_redis(token: str, phone_number: str):
    registration_token_redis.set(RedisKeyGenerator.get_registration_token_key(token),
                                 phone_number,
                                 ex=settings.REGISTRATION_TOKEN_TIME_TO_LIVE)


def get_registration_token(phone_number: str) -> str:
    token: str = generate_registration_token()
    add_token_to_redis(token, phone_number)
    return token
