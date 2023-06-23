import random
from typing import Optional

from django.conf import settings

from achare_interview.utils import exceptions
from achare_interview.utils.redis_client import validation_code_redis


class ValidationCode:
    fake_code: bool

    def __init__(self, fake_code: Optional[bool] = None):
        self.fake_code = fake_code if fake_code else settings.GENERATE_FAKE_CODE

    def generate_validation_code(self, phone_number: str) -> str:
        if self.fake_code:
            return phone_number[-6:]

        return random.choice("123456789") + ''.join(random.choices("01234567890", k=5))

    @staticmethod
    def get_code_key(phone_number: str) -> str:
        return f"{phone_number}_code"

    @staticmethod
    def get_phone_number_attempts_key(phone_number: str) -> str:
        return f"{phone_number}_attempts"

    @staticmethod
    def get_ip_attempts_key(ip: str) -> str:
        return f'{ip}_attempts'

    def get_attempts(self, key: str) -> int:
        redis_value: Optional[bytes] = validation_code_redis.get(key)
        attempt: int = 0
        if redis_value:
            attempt = int(redis_value)

        return attempt

    def add_code_to_redis(self, phone_number: str, code: str):
        validation_code_redis.set(self.get_code_key(phone_number),
                                  code,
                                  ex=settings.GENERATED_CODE_TIME_TO_LIVE)

    def add_phone_number_attempts_to_redis(self, phone_number: str, phone_number_attempts: int):
        validation_code_redis.set(self.get_phone_number_attempts_key(phone_number),
                                  phone_number_attempts + 1)

    def add_ip_attempts_to_redis(self, ip: str, ip_attempts: int):
        validation_code_redis.set(self.get_phone_number_attempts_key(ip),
                                  ip_attempts + 1)

    @staticmethod
    def check_phone_number_attempts(phone_number_attempts: int):
        if phone_number_attempts >= settings.MAXIMUM_CODE_REQUEST_COUNT:
            raise exceptions.MaximumPhoneNumberAttemptException()

    @staticmethod
    def check_ip_attempts(ip_attempts: int):
        if ip_attempts >= settings.MAXIMUM_CODE_REQUEST_COUNT:
            raise exceptions.MaximumIPAttemptException()

    def get_validation_code(self, phone_number: str, ip: str) -> str:
        phone_number_attempts: int = self.get_attempts(self.get_phone_number_attempts_key(phone_number))
        ip_attempts: int = self.get_attempts(self.get_ip_attempts_key(ip))

        self.check_phone_number_attempts(phone_number_attempts)
        self.check_ip_attempts(ip_attempts)

        generated_code: str = self.generate_validation_code(phone_number)
        self.add_code_to_redis(phone_number, generated_code)
        self.add_phone_number_attempts_to_redis(phone_number, phone_number_attempts)
        self.add_ip_attempts_to_redis(ip, ip_attempts)

        return generated_code
