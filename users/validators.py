import re

from django.core.exceptions import ValidationError


PHONE_PATTERN = re.compile(r"^(\+7|8)(\d{10})$")


def normalize_phone(value):
    digits = re.sub(r"\D", "", value or "")
    if len(digits) == 11 and digits.startswith("8"):
        return f"+7{digits[1:]}"
    if len(digits) == 11 and digits.startswith("7"):
        return f"+7{digits[1:]}"
    if len(digits) == 10:
        return f"+7{digits}"
    return value


def validate_phone_format(value):
    normalized = normalize_phone(value)
    if not PHONE_PATTERN.match(normalized):
        raise ValidationError(
            "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
        )
    return normalized


def validate_github_url(value):
    if not value:
        return value
    if "github.com" not in value.lower():
        raise ValidationError("Ссылка должна вести на GitHub.")
    return value
