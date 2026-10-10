from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from .models import (
    CODE_VERIFY,
    DONE,
    NEW,
    PHOTO_DONE,
    VIA_EMAIL,
    VIA_PHONE,
    CustomUser,
)
from .utils import check_input_type


class SignUpserializer(serializers.ModelSerializer):
    phone_number_email = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "auth_status", "auth_type", "phone_number_email"]
        read_only_fields = ["id", "auth_status", "auth_type"]

    def validate(self, attrs):
        value = attrs["phone_number_email"].strip()
        input_type = check_input_type(value)

        if input_type == "email":
            lookup = Q(email=value)
            user_data = {"email": value, "auth_type": VIA_EMAIL}
        elif input_type == "phone":
            lookup = Q(phone_number=value)
            user_data = {"phone_number": value, "auth_type": VIA_PHONE}
        else:
            raise serializers.ValidationError(
                "Telefon raqam yoki email noto'g'ri formatda."
            )

        user = CustomUser.objects.filter(lookup).first()
        if user and user.auth_status in (NEW, CODE_VERIFY):
            self._ensure_no_active_code(user)
            user.delete()
        elif user:
            raise serializers.ValidationError(
                "Bu email yoki telefon raqam allaqachon ro'yxatdan o'tgan."
            )

        return user_data

    @staticmethod
    def _ensure_no_active_code(user):
        has_active_code = user.codes.filter(
            used=False,
            expire_time__gte=timezone.now(),
        ).exists()
        if has_active_code:
            raise serializers.ValidationError(
                "Sizda hali amal qiladigan kod bor. Shu koddan foydalaning."
            )

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        code = user.generate_code(user.auth_type)

        if user.auth_type == VIA_EMAIL:
            from .mailer import send_verification_code

            send_verification_code(user.email, code)

        return user

    def to_representation(self, instance):
        return {
            "data": {
                "id": instance.id,
                "auth_status": instance.auth_status,
                "auth_type": instance.auth_type,
            },
            "token": instance.token(),
        }



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)



    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Eski parol noto'g'ri.")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Yangi parol kamida 8 ta belgidan iborat bo'lishi kerak.")

        if self.context['request'].user.check_password(value):
            raise serializers.ValidationError("Yangi parol eski parol bilan bir xil bo'lmasligi kerak.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()



class ChangePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["photo"]

    def update(self, instance, validated_data):
        if instance.auth_status != DONE:
            raise serializers.ValidationError(
                {"detail": "To'liq ro'yxatdan o'tmagansiz."}
            )

        instance.photo = validated_data["photo"]
        instance.auth_status = PHOTO_DONE
        instance.save(update_fields=["photo", "auth_status"])
        return instance


class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self._get_user(attrs["user_input"].strip())
        if user is None:
            raise serializers.ValidationError("Login yoki parol xato.")
        if user.auth_status in (NEW, CODE_VERIFY):
            raise serializers.ValidationError(
                "Siz to'liq ro'yxatdan o'tmagansiz."
            )

        authenticated_user = authenticate(
            username=user.username,
            password=attrs["password"],
        )
        if authenticated_user is None:
            raise serializers.ValidationError("Login yoki parol xato.")

        attrs["user"] = authenticated_user
        return attrs

    @staticmethod
    def _get_user(user_input):
        if user_input.startswith("+998"):
            lookup = Q(phone_number=user_input)
        elif "@" in user_input:
            lookup = Q(email=user_input.lower())
        else:
            lookup = Q(username=user_input)
        return CustomUser.objects.filter(lookup).first()

    def to_representation(self, instance):
        return {"token": instance["user"].token()}





class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "photo"]
        read_only_fields = ["username"]








