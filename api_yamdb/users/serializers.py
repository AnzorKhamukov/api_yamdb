from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Cериалайзер кастомного пользователя."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер регистрации пользователей."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" недоступно'
            )
        if User.objects.filter(email=data['email'],
                               username=data['username']).exists():
            return data
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Этот email уже используется')
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Это имя уже занято.')

        return data


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериалайзер получения токена для пользователей."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
