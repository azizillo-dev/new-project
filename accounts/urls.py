from django.urls import path

from .views import ChangeInfoView, ChangePhotoView, ForgotPasswordView, ForgotPassword, GetNewCodeView, LogoutView, LogoutView, LogoutViewView, Ge, LogoutView, PasswordCh, PasswordChangeView, PasswordChangeViewangeView, PasswordCh, PasswordChangeViewangeViewtNewCodeView, ResetPasswordView, ResetPasswordView, ProfileUpdateView, SignUpView, VerifyCodeView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify-code"),
    path("get-new-code/", GetNewCodeView.as_view(), name="get-new-code"),
    path("change-info/", ChangeInfoView.as_view(), name="change-info"),
    path("change-photo/", ChangePhotoView.as_view(), name="change-photo"),
    path("profile-update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("password-change/", PasswordChangeView.as_view(), name="password-change"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),    
]
