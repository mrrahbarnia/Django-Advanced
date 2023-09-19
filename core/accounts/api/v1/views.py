from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken import views, models
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from mail_templated import EmailMessage

import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    DecodeError,
)

from decouple import config

from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    EmailActivationResendSerializer,
    RePasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
)

from ...models import Profile
from ..utils import EmailThread

User = get_user_model()  # User model


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data["email"]
        data = {"email": email}
        user_object = get_object_or_404(User, email=email)
        token = self.get_tokens_for_user(user_object)
        message = EmailMessage(
            "email/activation-email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[email],
        )
        EmailThread(message).start()
        return Response(data, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(views.ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = models.Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "email": user.email}
        )


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomChangePassword(generics.GenericAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        object = self.request.user
        return object

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.object.check_password(
            serializer.data.get("old_password")
        ):
            return Response(
                {"old_password": "Wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()
        return Response(
            {"details": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class EmailActivationAPIView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(
                token, config("SECRET_KEY"), algorithms=["HS256"]
            )
            user_id = token.get("user_id")
        except InvalidSignatureError:
            return Response(
                {"detail": "Token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = get_object_or_404(User, pk=user_id)
        if user_obj.is_verified:
            return Response(
                {"detail": "Your account has been already verified"}
            )
        else:
            user_obj.is_verified = True
            user_obj.save()
            return Response(
                {"detail": "Your account has been verified successfully"}
            )


class EmailActivationResendAPIView(generics.GenericAPIView):
    serializer_class = EmailActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = EmailActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_object = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_object)
        message = EmailMessage(
            "email/activation-email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_object.email],
        )
        EmailThread(message).start()
        return Response(
            {"detail": "The verificatione email resent successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class RePasswordEmailRequestApiView(generics.GenericAPIView):
    serializer_class = RePasswordEmailRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = (RefreshToken.for_user(user)).access_token
        site = get_current_site(request=request).domain
        relative_link = "/accounts/api/v1/reset-password/" + str(token)
        message = EmailMessage(
            "email/reset-password.tpl",
            {"link": "http://" + site + relative_link, "user": user.email},
            "admin@admin.com",
            to=[user.email],
        )
        EmailThread(message).start()
        return Response({"detail": "The email has been sent for you."})


class RePasswordValidateTokenApiView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.__dict__["parser_context"].get("kwargs").get("token")
        try:
            token = jwt.decode(
                token, config("SECRET_KEY"), algorithms=["HS256"]
            )
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "Token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DecodeError:
            return Response(
                {"detail": "Token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "The token is valid"}, status=status.HTTP_200_OK
        )


class RePasswordSetNewPasswordApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"detail": "Password reset successfully"},
            status=status.HTTP_200_OK,
        )
