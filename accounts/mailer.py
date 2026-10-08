from django.core.mail import send_mail


def send_verification_code(email, code):
    send_mail(
        subject='Tasdiqlash kodi',
        message=f"Ro'yxatdan o'tishni tasdiqlash kodingiz: {code}",
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )
