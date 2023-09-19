import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import jwt
from jwt.exceptions import (
    InvalidSignatureError,
    ExpiredSignatureError,
    DecodeError,
)

from decouple import config

from ...models import User, Profile


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=6)
    password = serializers.CharField(max_length=250)
    password1 = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError(
                {"detail": "passwrods doesnt match"}
            )
        try:
            validators.validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")
        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _(
                    "No active account found with the given credentials. "
                )
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError(
                    {"detail": "The user is not verified"}
                )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError(
                {"detail": "The user is not verified"}
            )
        validate_data["email"] = self.user.email
        validate_data["user_id"] = self.user.id
        return validate_data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError(
                {"detail": "passwrods doesnt match"}
            )
        try:
            validators.validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "email", "first_name", "last_name", "description"]


class EmailActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        # try:
        user_object = User.objects.get(email=email)
        # except User.DoesNotExist:
        #     return serializers.ValidationError(
        #         {"detail":"user doesnt exist"}
        #         )
        if user_object.is_verified:
            return serializers.ValidationError(
                {"detail": "user has already been verified and activated. "}
            )
        attrs["user"] = user_object
        return super().validate(attrs)


class RePasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs["email"]
        try:
            validated_data = super().validate(attrs)
            user = User.objects.get(email=email)
            validated_data["user"] = user
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "There is no user with provided email."}
            )
        return validated_data


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8, max_length=20, required=True
    )
    password1 = serializers.CharField(
        min_length=8, max_length=20, required=True
    )
    token = serializers.CharField(max_length=600, required=True)

    class Meta:
        fields = ["password", "password1", "token"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError(
                {"detail": "passwrods doesnt match"}
            )
        try:
            validators.validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        try:
            token = jwt.decode(
                attrs.get("token"), config("SECRET_KEY"), algorithms=["HS256"]
            )
            user = User.objects.get(id=token["user_id"])
        except ExpiredSignatureError:
            raise serializers.ValidationError(
                {"detail": "The token has been expired."}
            )
        except InvalidSignatureError:
            raise serializers.ValidationError(
                {"detail": "The token is not valid."}
            )
        except DecodeError:
            raise serializers.ValidationError(
                {"detail": "The token is not valid."}
            )
        user.set_password(attrs["password"])
        user.save()
        return super().validate(attrs)
