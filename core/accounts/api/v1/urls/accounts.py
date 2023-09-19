from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .. import views


urlpatterns = [
    # Registration
    path(
        "registration/",
        views.RegistrationAPIView.as_view(),
        name="registration",
    ),
    # Email activation
    path(
        "activation/<str:token>",
        views.EmailActivationAPIView.as_view(),
        name="email-activation",
    ),
    # Resend email verification
    path(
        "activation/resend/",
        views.EmailActivationResendAPIView.as_view(),
        name="email-activation-resend",
    ),
    # Change password
    path(
        "change-password/",
        views.CustomChangePassword.as_view(),
        name="change=password",
    ),
    # Reset password
    path(
        "reset-password/",
        views.RePasswordEmailRequestApiView.as_view(),
        name="reset-password",
    ),
    path(
        "reset-password/<str:token>/",
        views.RePasswordValidateTokenApiView.as_view(),
        name="reset-password-validate",
    ),
    path(
        "reset-password/set-password/",
        views.RePasswordSetNewPasswordApiView.as_view(),
        name="reset-password-confirm",
    ),
    # Login Token
    path(
        "token/login/",
        views.CustomObtainAuthToken.as_view(),
        name="token-login",
    ),
    path(
        "token/logout/",
        views.CustomDiscardAuthToken.as_view(),
        name="token-logout",
    ),
    # Login JWT
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
