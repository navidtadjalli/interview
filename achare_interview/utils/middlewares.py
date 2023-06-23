from django.conf import settings
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


class AttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: WSGIRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # print(request.path in settings.SENSITIVE_ENDPOINTS)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
