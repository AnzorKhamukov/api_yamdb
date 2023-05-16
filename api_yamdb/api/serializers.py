from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """Cериалайзер кастомного пользователя."""
    user = serializers.SlugRelatedField(
        required=True,
        slug_field='username',
    )
    email = serializers.EmailField(
        required=True,
        slug_field='email',
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
            )
        read_only_fields = ('role')


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер регистрации пользователей."""
    username = serializers.CharField(slug_field='username', required=True)
    email = serializers.EmailField(slug_field='email', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериалайзер получения токена для пользователей."""
    username = serializers.CharField()
    confitmation_code = serializers.CharField()
