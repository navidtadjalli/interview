class ValidationCodeExpiredException(Exception):
    pass


class ValidationCodeDoesNotMatchException(Exception):
    pass


class RegistrationTokenIsNotValidException(Exception):
    pass


class MaximumAttemptException(Exception):
    pass


class PhoneNumberHasBeenBlockedException(Exception):
    pass


class IPHasBeenBlockedException(Exception):
    pass