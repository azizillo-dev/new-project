from django.db import models
from baseapp.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


NEW, CODE_VERIFY, DONE, PHOTO_DONE = ('new', 'code_verify', 'done', 'photo_done')
VIA_PHONE, VIA_EMAIL = ('via_phone', 'via_email')
CUSTOMER, SELLER = ('customer', 'seller')
AUTH_TYPE = ('via_email', 'via_phone')



EMAIL_EXPARATION_TIME = 5
PHONE_EXPARATION_TIME = 3


class CustomUSer(BaseModel, AbstractUser):

    USER_ROLE = (
        (CUSTOMER, CUSTOMER),
        (SELLER, SELLER)
    )

    AUTH_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )

    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFY, CODE_VERIFY),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE)
    )


    user_role = models.CharField(max_length=31, choices=USER_ROLE, default=CUSTOMER)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    auth_type = models.CharField(max_length=10, choices=AUTH_TYPE)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='accounts/', blank=True, null=True)


class Verify(BaseModel):

    VERIFY_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )

    auth_type = models.CharField(max_length=31, choices=VERIFY_TYPE)
    code = models.CharField(max_length=4)
    user = models.ForeignKey(CustomUSer, on_delete=models.CASCADE, related_name='codes')
    expire_time = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"code: {self.code} | user: {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.auth_type == VIA_EMAIL:
                self.expire_time = timezone.now() + timedelta(minutes=EMAIL_EXPARATION_TIME)
            elif self.auth_type == VIA_PHONE:
                self.expire_time = timezone.now() + timedelta(minutes=PHONE_EXPARATION_TIME)
        super().save(*args, **kwargs)        








