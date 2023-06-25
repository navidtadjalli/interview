import json

from django.core.handlers.wsgi import WSGIRequest


# def get_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#
#     return ip
#
#
# def get_attempts(key: str) -> int:
#     redis_value: Optional[bytes] = validation_code_redis.get(key)
#     attempt: int = 0
#     if redis_value:
#         attempt = int(redis_value)
#
#     return attempt
#
# def add_phone_number_attempts_to_redis(phone_number: str, phone_number_attempts: int):
#     validation_code_redis.set(RedisKeyGenerator.get_phone_number_attempts_key(phone_number),
#                               phone_number_attempts + 1)
#
#
# def add_ip_attempts_to_redis(ip: str, ip_attempts: int):
#     validation_code_redis.set(RedisKeyGenerator.get_phone_number_attempts_key(ip),
#                               ip_attempts + 1)
#
#
# def check_phone_number_attempts(phone_number_attempts: int):
#     if phone_number_attempts >= settings.MAXIMUM_CODE_REQUEST_COUNT:
#         raise exceptions.MaximumPhoneNumberAttemptException()
#
#
# def check_ip_attempts(ip_attempts: int):
#     if ip_attempts >= settings.MAXIMUM_CODE_REQUEST_COUNT:
#         raise exceptions.MaximumIPAttemptException()
from django.urls import reverse

from achare_interview.utils.redis_utils import key_generators
from achare_interview.utils.redis_utils.redis_client import attempts_redis


class AttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: WSGIRequest):
        if request.path == reverse("authenticate"):
            if request.body:
                body_dict: dict = json.loads(request.body)
                phone_number: str = body_dict["phone_number"]
                attempts_redis.set(key_generators.get_phone_number_attempts_key(phone_number), "1")

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # print(request.path in settings.SENSITIVE_ENDPOINTS)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
