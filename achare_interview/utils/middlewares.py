import json
from http import HTTPStatus
from typing import Optional

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse

from rest_framework.response import Response

from achare_interview.utils import error_messages, exceptions
from achare_interview.utils.redis_utils import attempts_count, blocked, key_generators


class AttemptMiddleware:
    def __init__(self, get_response):
        self.request_sensitive_path_list = list(map(reverse, settings.REQUEST_SENSITIVE_ENDPOINTS_NAMES))
        self.response_sensitive_path_list = list(map(reverse, settings.RESPONSE_SENSITIVE_ENDPOINTS_NAMES))
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        request_path: str = ""
        ip: str = ""
        phone_number: str = ""

        if request.path in self.request_sensitive_path_list + self.response_sensitive_path_list:
            request_path = request.path
            phone_number = self.get_phone_number(request)
            ip = self.get_client_ip(request)

        try:
            self.do_pre_request_stuff(request_path, ip, phone_number)
        except exceptions.MaximumAttemptException:
            return Response(error_messages.REQUESTED_MORE_THAN_3_TIMES_ERROR_MESSAGE, status=HTTPStatus.FORBIDDEN)
        except exceptions.PhoneNumberHasBeenBlockedException:
            return Response(error_messages.PHONE_NUMBER_HAS_BEEN_BLOCKED_ERROR_MESSAGE, status=HTTPStatus.FORBIDDEN)
        except exceptions.IPHasBeenBlockedException:
            return Response(error_messages.IP_HAS_BEEN_BLOCKED_ERROR_MESSAGE, status=HTTPStatus.FORBIDDEN)

        response = self.get_response(request)

        self.do_post_request_stuff(response, request_path, ip, phone_number)

        return response

    @staticmethod
    def get_client_ip(request: WSGIRequest) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_phone_number(request: WSGIRequest) -> str:
        if request.body:
            body_dict: dict = json.loads(request.body)
            return body_dict["phone_number"]

        return ""

    def block_key(self, key: str):
        blocked.set_block_key(key)

    def check_if_key_is_blocked(self, key: str):
        if blocked.is_key_blocked(key):
            raise exceptions.KeyHasBeenBlockedException()

    def check_attempts(self, key: str, block_key: str):
        current_attempts: int = attempts_count.get_attempts(key)

        if current_attempts >= settings.MAXIMUM_CODE_REQUEST_COUNT:
            self.block_key(block_key)
            raise exceptions.MaximumAttemptException()

        attempts_count.set_attempts(key, current_attempts + 1)

    def check_ip_attempts(self, ip: str):
        try:
            self.check_if_key_is_blocked(key_generators.get_blocked_key_for_ip(ip))
        except exceptions.KeyHasBeenBlockedException:
            raise exceptions.IPHasBeenBlockedException()

        self.check_attempts(key_generators.get_ip_attempts_key_for_authenticate(ip),
                            key_generators.get_blocked_key_for_ip(ip))

    def check_phone_number_attempts(self, phone_number: str):
        try:
            self.check_if_key_is_blocked(key_generators.get_blocked_key_for_phone_number(phone_number))
        except exceptions.KeyHasBeenBlockedException:
            raise exceptions.PhoneNumberHasBeenBlockedException()

        self.check_attempts(key_generators.get_phone_number_attempts_key_for_authenticate(phone_number),
                            key_generators.get_blocked_key_for_phone_number(phone_number))

    def do_pre_request_stuff(self, request_path: str, ip: str, phone_number: str):
        if request_path in self.request_sensitive_path_list:
            self.check_ip_attempts(ip)

            if phone_number:
                self.check_phone_number_attempts(phone_number)

    # def remove_attempts(self, ip: str, phone_number: str):
    #     blocked.delete_ip_attempts(ip)
    #     blocked.delete_phone_number_attempts(ip)

    def do_post_request_stuff(self, response: Response, request_path: str, ip: str, phone_number: str):
        if request_path in self.response_sensitive_path_list:
            if request_path == reverse("validate"):
                if response.status_code == HTTPStatus.BAD_REQUEST and \
                        response.data == error_messages.VALIDATION_CODE_DOES_NOT_MATCH_ERROR_MESSAGE:
                    current_phone_number_attempts_count: int = attempts_count.get_attempts_for_phone_number_for_validate(
                        phone_number)
                    attempts_count.set_attempts_for_phone_number_for_validate(phone_number, current_phone_number_attempts_count + 1)

                    current_ip_attempts_count: int = attempts_count.get_attempts_for_ip_for_validate(
                        ip)
                    attempts_count.set_attempts_for_ip_for_validate(ip, current_ip_attempts_count + 1)
