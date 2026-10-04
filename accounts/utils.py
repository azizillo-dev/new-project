import re

phone_regex = re.compile(r'^\+998\d{9}$')
email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


def email_or_phone_number(value):
    if re.fullmatch(phone_regex, value):
        return 'phone_number'
    elif re.fullmatch(email_regex, value):
        return 'email'
    raise ValueError('Email yoki telefon raqam notogri formatda kiritilgan')

