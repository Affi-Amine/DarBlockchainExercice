from django.core.exceptions import ValidationError
import re

class UppercaseValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError("The password must contain at least one uppercase letter.")

    def get_help_text(self):
        return "Your password must contain at least one uppercase letter."

class NumberValidator:
    def validate(self, password, user=None):
        if not re.search(r'[0-9]', password):
            raise ValidationError("The password must contain at least one number.")

    def get_help_text(self):
        return "Your password must contain at least one number."

class SymbolValidator:
    def validate(self, password, user=None):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("The password must contain at least one symbol.")

    def get_help_text(self):
        return "Your password must contain at least one symbol."