import re

PHONE_REGEX = re.compile(r'^\+998\d{9}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

def check_input_type(value):
    value = value.strip()
    if PHONE_REGEX.fullmatch(value):
        return 'phone'
    if EMAIL_REGEX.fullmatch(value):
        return 'email'
    return None   # xatoni serializer ko'taradi