import random
from typing import Optional

from django.conf import settings

from achare_interview.utils.redis_client import validation_code_redis


class ValidationCode:
    fake_code: bool

    def __init__(self, fake_code: Optional[bool] = None):
        self.fake_code = fake_code if fake_code else settings.GENERATE_FAKE_CODE

    def generate_validation_code(self, phone_number: str) -> str:
        if self.fake_code:
            return phone_number[-6:]

        return random.choice("123456789") + ''.join(random.choices("01234567890", k=5))

    def add_code_to_redis(self, phone_number: str, code: str):
        validation_code_redis.set(phone_number, code, ex=settings.GENERATED_CODE_TIME_TO_LIVE)

    def get_validation_code(self, phone_number: str) -> str:
        generated_code: str = self.generate_validation_code(phone_number)
        self.add_code_to_redis(phone_number, generated_code)

        return generated_code
