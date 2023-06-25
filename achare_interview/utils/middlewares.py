import json
from http import HTTPStatus

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse

from rest_framework.response import Response

from achare_interview.utils import error_messages, exceptions
from achare_interview.utils.redis_utils import attempts_count, blocked


class AttemptMiddleware:
    def __init__(self, get_response):
        self.path_list = list(map(reverse, settings.SENSITIVE_ENDPOINTS_NAMES))
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        try:
            self.do_pre_request_stuff(request)
        except exceptions.MaximumAttemptException:
            return Response(error_messages.REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE, status=HTTPStatus.FORBIDDEN)
        except exceptions.PhoneNumberHasBeenBlockedException:
            return Response(error_messages.PHONE_NUMBER_HAS_BEEN_BLOCKED_ERROR_MESSAGE, status=HTTPStatus.FORBIDDEN)
        except exceptions.IPHasBeenBlockedException:
            return Response(error_messages.IP_HAS_BEEN_BLOCKED_ERROR_MESSAGE, status=HTTPStatus.FORBIDDEN)

        response = self.get_response(request)



        return response

    @staticmethod
    def get_client_ip(request: WSGIRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def block_ip(self, ip: str):
        blocked.set_block_key_for_ip(ip)

    def check_if_ip_is_blocked(self, phone_number: str):
        if blocked.is_ip_blocked(phone_number):
            raise exceptions.IPHasBeenBlockedException()

    def check_ip_attempts(self, request: WSGIRequest):
        ip: str = self.get_client_ip(request)

        self.check_if_ip_is_blocked(ip)

        current_ip_attempts_count: int = attempts_count.get_attempts_for_ip(ip)

        if current_ip_attempts_count >= settings.MAXIMUM_CODE_REQUEST_COUNT:
            self.block_ip(ip)
            raise exceptions.MaximumAttemptException()

        attempts_count.set_attempts_for_ip(ip,
                                           current_ip_attempts_count + 1)

    def block_phone_number(self, phone_number: str):
        blocked.set_block_key_for_phone_number(phone_number)

    def check_if_phone_number_is_blocked(self, phone_number: str):
        if blocked.is_phone_number_blocked(phone_number):
            raise exceptions.PhoneNumberHasBeenBlockedException()

    def check_phone_number_attempts(self, request: WSGIRequest):
        body_dict: dict = json.loads(request.body)
        phone_number: str = body_dict["phone_number"]

        self.check_if_phone_number_is_blocked(phone_number)

        current_attempts_count: int = attempts_count.get_attempts_for_phone_number(phone_number)

        if current_attempts_count >= settings.MAXIMUM_CODE_REQUEST_COUNT:
            self.block_phone_number(phone_number)
            raise exceptions.MaximumAttemptException()

        attempts_count.set_attempts_for_phone_number(phone_number,
                                                     current_attempts_count + 1)

    def do_pre_request_stuff(self, request: WSGIRequest):
        if request.path in self.path_list:
            self.check_ip_attempts(request)

            if request.body:
                self.check_phone_number_attempts(request)
