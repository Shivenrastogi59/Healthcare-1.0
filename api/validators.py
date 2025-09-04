from django.core.exceptions import ValidationError


def validate_age(value: int):
    if value < 0 or value > 130:
        raise ValidationError("Age must be between 0 and 130.")