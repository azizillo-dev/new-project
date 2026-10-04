from rest_framework import serializers
from .utils import email_or_phone_number
from .models import CustomUser, Verify
from accounts.models import VIA_EMAIL, VIA_PHONE_NUMBER


class SignUpSerializer(serializers.ModelSerializer):

    phone_number_email = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'auth_status', 'auth_type']
        read_only_fields = fields


    def validate(self, data):
        phone_number_email = data.get('phone_number_email')
        phone_number_or_email = email_or_phone_number(phone_number_email)

        if phone_number_or_email == 'phone_number':
            return {
                "phone_number": phone_number_email,
                "auth_type": VIA_PHONE_NUMBER
            }
        elif phone_number_or_email == 'email':
            return {
                "email": phone_number_email,
                "auth_type": VIA_EMAIL
            }
        raise ValueError('Email yoki telefon raqam notogri formatda kiritilgan')
