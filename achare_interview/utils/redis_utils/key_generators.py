def get_code_key(phone_number: str) -> str:
    return f"{phone_number}_code"


def get_registration_token_key(token) -> str:
    return token


def get_phone_number_attempts_key_for_authenticate(phone_number: str) -> str:
    return f"{phone_number}_authenticate_attempts"


def get_ip_attempts_key_for_authenticate(ip: str) -> str:
    return f'{ip}_authenticate_attempts'


def get_blocked_key_for_phone_number(phone_number: str) -> str:
    return f'{phone_number}_blocked'


def get_blocked_key_for_ip(ip: str) -> str:
    return f'{ip}_blocked'


def get_phone_number_attempts_key_for_validate(phone_number: str) -> str:
    return f"{phone_number}_validate_attempts"


def get_ip_attempts_key_for_validate(ip: str) -> str:
    return f'{ip}_validate_attempts'

