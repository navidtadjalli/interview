from uuid import uuid4

from django.conf import settings

from achare_interview.utils import exceptions
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


def get_token_value_from_redis(token: str) -> str:
    redis_value: bytes = registration_token_redis.get(RedisKeyGenerator.get_registration_token_key(token))
    if not redis_value:
        raise exceptions.RegistrationTokenIsNotValidException()

    return redis_value.decode(encoding="utf-8")


def delete_token_from_redis(token: str):
    registration_token_redis.delete(RedisKeyGenerator.get_registration_token_key(token))


def validate_registration_token(phone_number: str, token: str):
    redis_value: str = get_token_value_from_redis(token)

    if redis_value != phone_number:
        raise exceptions.RegistrationTokenIsNotValidException()

    delete_token_from_redis(token)
