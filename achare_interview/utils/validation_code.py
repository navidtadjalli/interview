import random
from typing import Optional

from django.conf import settings

from achare_interview.utils.redis_client import validation_code_instance


class ValidationCode:
    fake_code: bool

    def __init__(self, fake_code: Optional[bool] = None):
        self.fake_code = fake_code if fake_code else settings.GENERATE_FAKE_CODE

    def get_validation_code(self, phone_number: str) -> str:
        if self.fake_code:
            return phone_number[-6:]

        return random.choice("123456789") + ''.join(random.choices("01234567890", k=5))
