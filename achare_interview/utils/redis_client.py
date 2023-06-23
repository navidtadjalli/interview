from django.conf import settings
import redis

validation_code_redis: redis.Redis = redis.Redis(host=settings.REDIS_HOST,
                                                 port=settings.REDIS_PORT,
                                                 db=settings.REDIS_VALIDATION_CODE_DB)


def reset_redis(client: redis.Redis):
    for key in client.scan_iter("*"):
        client.delete(key)


class RedisKeyGenerator:
    @staticmethod
    def get_code_key(phone_number: str) -> str:
        return f"{phone_number}_code"

    @staticmethod
    def get_phone_number_attempts_key(phone_number: str) -> str:
        return f"{phone_number}_attempts"

    @staticmethod
    def get_ip_attempts_key(ip: str) -> str:
        return f'{ip}_attempts'