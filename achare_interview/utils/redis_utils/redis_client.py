from django.conf import settings
import redis

validation_code_redis: redis.Redis = redis.Redis(host=settings.REDIS_HOST,
                                                 port=settings.REDIS_PORT,
                                                 db=settings.REDIS_VALIDATION_CODE_DB)

registration_token_redis: redis.Redis = redis.Redis(host=settings.REDIS_HOST,
                                                    port=settings.REDIS_PORT,
                                                    db=settings.REDIS_VALIDATION_CODE_DB)

attempts_redis: redis.Redis = redis.Redis(host=settings.REDIS_HOST,
                                          port=settings.REDIS_PORT,
                                          db=settings.REDIS_ATTEMPTS_DB)

blocked_redis: redis.Redis = redis.Redis(host=settings.REDIS_HOST,
                                         port=settings.REDIS_PORT,
                                         db=settings.REDIS_BLOCKED_DB)


def reset_redis(client: redis.Redis):
    for key in client.scan_iter("*"):
        client.delete(key)
