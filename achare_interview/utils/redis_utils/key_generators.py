def get_code_key(phone_number: str) -> str:
    return f"{phone_number}_code"


def get_registration_token_key(token) -> str:
    return token


def get_phone_number_attempts_key(phone_number: str) -> str:
    return f"{phone_number}_attempts"


def get_ip_attempts_key(ip: str) -> str:
    return f'{ip}_attempts'


def get_blocked_key_for_phone_number(phone_number: str) -> str:
    return f'{phone_number}_blocked'


def get_blocked_key_for_ip(ip: str) -> str:
    return f'{ip}_blocked'
