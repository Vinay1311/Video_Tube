from django.core.validators import RegexValidator
from helper import messages


# ------------------ Regex's ---------------- #

phone_number_regex = RegexValidator(regex=r'^[6-9]\d{9}$', message=messages.PHONE_NUMBER_INCORRECT)

email_regex = RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', message=messages.EMAIL_NOT_CORRECT)
