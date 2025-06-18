"""User serializer for handling user data in the API."""

from typing import ClassVar

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Meta class for UserSerializer."""

        model = User
        fields: ClassVar = ["id", "username", "email", "password", "first_name", "last_name"]
        extra_kwargs: ClassVar = {
            "email": {"required": True},
            "username": {"required": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict) -> User:
        """Create a new user instance."""
        # Handles user registration (with password hashing)
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        """Update an existing user instance."""
        # Handles profile update
        password = validated_data.pop("password", None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update password separately
        if password:
            instance.set_password(password)

        instance.save()
        return instance

