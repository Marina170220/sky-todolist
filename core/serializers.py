from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        read_only_fields = ("id", )
        fields = ("id", "username", "first_name", "last_name", "email", "password", "password_repeat")

    def validate(self, attrs: dict):
        password: Optional[str] = attrs.get("password")
        password_repeat: str = attrs.pop("password_repeat", None)
        if password != password_repeat:
            raise ValidationError("Passwords are not equal")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        self.user = user
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ("id", )
        fields = ("id", "username", "first_name", "last_name", "email")


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True, write_only=True)
    password=serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict) -> dict:
        username: Optional[str] = attrs.get("username")
        password: Optional[str] = attrs.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("Invalid username or password")
        attrs["user"] = user
        return attrs


class PasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        read_only_fields = ("id", )
        fields = ("old_password", "new_password")

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        user: User = self.instance
        if not user.check_password(old_password):
            raise ValidationError({"old_password": "incorrect field"})
        return attrs

    def update(self, instance: User, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance
