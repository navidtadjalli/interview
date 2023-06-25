import json
from http import HTTPStatus

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
from django.urls import reverse
from rest_framework.response import Response

from achare_interview.utils import error_messages, exceptions
from achare_interview.utils.redis_utils import key_generators, attempts_count
from achare_interview.utils.redis_utils.redis_client import attempts_redis


class AttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: WSGIRequest):
        try:
            self.do_pre_request_stuff(request)
        except exceptions.MaximumPhoneNumberAttemptException:
            return Response(error_messages.IP_HAS_BEEN_BLOCKED_ERROR_MESSAGE, status=HTTPStatus.FORBIDDEN)

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # print(request.path in settings.SENSITIVE_ENDPOINTS)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    @staticmethod
    def get_client_ip(request: WSGIRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def do_pre_request_stuff(self, request: WSGIRequest):
        if request.path == reverse("authenticate"):
            ip: str = self.get_client_ip(request)

            current_ip_attempts_count: int = attempts_count.get_attempts_for_ip(ip)

            if current_ip_attempts_count >= settings.MAXIMUM_CODE_REQUEST_COUNT:
                raise exceptions.MaximumPhoneNumberAttemptException()

            attempts_count.set_attempts_for_ip(ip,
                                               current_ip_attempts_count + 1)

            if request.body:
                body_dict: dict = json.loads(request.body)
                phone_number: str = body_dict["phone_number"]
                current_attempts_count: int = attempts_count.get_attempts_for_phone_number(phone_number)

                if current_attempts_count >= settings.MAXIMUM_CODE_REQUEST_COUNT:
                    raise exceptions.MaximumPhoneNumberAttemptException()

                attempts_count.set_attempts_for_phone_number(phone_number,
                                                             current_attempts_count + 1)
