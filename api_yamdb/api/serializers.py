from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """Cериалайзер кастомного пользователя."""
    username = serializers.CharField(required=True)
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
        fields = ('username', 'email')

    def validate_data(self, value):
        if User.objects.filter(username=value).exists():
            return serializers.ValidationError('Это имя уже занято.')
        if User.objects.filter(email=value).exists():
            return serializers.ValidationError('Этот email уже используется')
        return value


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериалайзер получения токена для пользователей."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
