from django.core.mail import send_mail
from django.conf import settings


def send_verification_code(email, code):
    send_mail(
        subject="Tasdiqlash kodi",
        message=f"Ro'yxatdan o'tishni tasdiqlash kodingiz: {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
