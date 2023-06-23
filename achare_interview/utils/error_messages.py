from django.utils.translation import gettext_lazy as _


def get_error_dict(msg: str) -> dict:
    return {
        "detail": msg
    }


VALIDATION_CODE_DOES_NOT_MATCH_ERROR_MESSAGE = get_error_dict(_("Validation code does not match."))
VALIDATION_CODE_EXPIRED_ERROR_MESSAGE = get_error_dict(_("Validation code expired."))
