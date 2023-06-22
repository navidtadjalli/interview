from django.conf import settings
import redis

validation_code_instance = redis.Redis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_VALIDATION_CODE_DB)
