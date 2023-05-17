from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """Cериалайзер кастомного пользователя."""

    email = serializers.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
            )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер регистрации пользователей."""
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериалайзер получения токена для пользователей."""
    username = serializers.CharField()
    confitmation_code = serializers.CharField()
