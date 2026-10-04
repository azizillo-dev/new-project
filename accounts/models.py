import uuid, random
from django.db import models
from baseapp.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError
import uuid, random
from rest_framework_simplejwt.tokens import RefreshToken

from conf import settings


NEW, CODE_VERIFY, DONE, PHOTO_DONE = ('new', 'code_verify', 'done', 'photo_done')
VIA_PHONE, VIA_EMAIL = ('via_phone', 'via_email')
CUSTOMER, SELLER = ('customer', 'seller')


class CustomUser(BaseModel, AbstractUser):

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

    email = models.EmailField(unique=True, null=True, blank=True)
    user_role = models.CharField(max_length=31, choices=USER_ROLE, default=CUSTOMER)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    auth_type = models.CharField(max_length=10, choices=AUTH_TYPE)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='accounts/', blank=True, null=True)


    def generate_code(self):
        return str(random.randint(1000, 9999))

    
    def check_email(self):
        if CustomUser.objects.filter(username=self.email).exists():
            raise ValidationError("Bu email band")
        return


    def check_username(self):
        if not self.username:
            ud = str(uuid.uuid4)
            temp_username = "username" + ud[int(ud.rfind("-")) + 1: ]
            while CustomUser.objects.filter(username=temp_username).exists():
                temp_username = temp_username + str(random.randint(0, 10))
            self.username = temp_username

    def check__password(self):
        if not self.password:
            ud = str(uuid.uuid4)
            temp_password = "password" + ud[int(ud.rfind("-")) + 1: ]
            self.password = temp_password

    def check_hashing_pass(self):
        if not self.password.startswith("pbkdf2_sha256$"):
            self.set_password(self.password)

    def check_email_normalize(self):
        if self.email:
            temp = self.email.lower()
            self.email = temp

    @property
    def token(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            "refresh_token" : str(refresh_token),
            "access_token" : str(refresh_token.access_token)
        }


    def save(self, *args, **kwargs):
        self.check_email_normalize()
        self.check_email()
        self.check_username()
        self.check__password()
        self.check_hashing_pass()
        super().save(*args, **kwargs)



class Verify(BaseModel):

    VERIFY_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )

    auth_type = models.CharField(max_length=31, choices=VERIFY_TYPE)
    code = models.CharField(max_length=4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='codes')
    expire_time = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"code: {self.code} | user: {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.auth_type == VIA_EMAIL:
                self.expire_time = timezone.now() + timedelta(minutes=settings.EMAIL_EXPIRATION_TIME)
            elif self.auth_type == VIA_PHONE:
                self.expire_time = timezone.now() + timedelta(minutes=settings.PHONE_EXPIRATION_TIME)
        super().save(*args, **kwargs)        
















