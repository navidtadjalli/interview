import json
from collections import Callable

from rest_framework.test import APITestCase
from achare_interview.utils.redis_utils import redis_client


class CustomAPITestCase(APITestCase):
    GET_METHOD_TYPE: str = "GET"
    POST_METHOD_TYPE: str = "POST"

    @staticmethod
    def reset_redis():
        redis_client.reset_redis(redis_client.validation_code_redis)
        redis_client.reset_redis(redis_client.registration_token_redis)
        redis_client.reset_redis(redis_client.attempts_redis)

    def call_endpoint(self, url: str, method: str, data: dict = None):
        callable_method: Callable = self.client.get

        if method == self.GET_METHOD_TYPE:
            callable_method = self.client.get
        if method == self.POST_METHOD_TYPE:
            callable_method = self.client.post

        callable_arguments = {
            "path": url,
            "content_type": "application/json"
        }

        if data:
            callable_arguments["data"] = json.dumps(data)

        return callable_method(**callable_arguments)

    def call_endpoint_with_get(self, url: str, data: dict = None):
        return self.call_endpoint(url, self.GET_METHOD_TYPE, data=data)

    def call_endpoint_with_post(self, url: str, data: dict = None):
        return self.call_endpoint(url, self.POST_METHOD_TYPE, data=data)
