from wtforms import ValidationError

class CustomPasswordValidator(object):
    def __init__(self):
        self.message = 'Password must have at least one upper letter and at least one symbol and at least one number and no space'

    def __call__(self, form, field):
        text : str = field.data
        is_any_numbers = any(x.isdigit() for x in text)
        is_any_upper = any(x.isupper() for x in text)
        is_any_symbol = any(not x.isalnum() for x in text)
        is_any_space = any(x.isspace() for x in text)

        if not (is_any_numbers and is_any_upper and is_any_symbol) or is_any_space:
            raise ValidationError(self.message)