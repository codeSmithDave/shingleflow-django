from django.core.validators import RegexValidator

postal_code_validator = RegexValidator(
 regex=r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$",
 message="Postal code must be in the format A1A 1A1",
)