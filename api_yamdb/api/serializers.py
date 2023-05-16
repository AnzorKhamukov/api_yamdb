from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
            )


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(slug_field='username', required=True)
    email = serializers.EmailField(slug_field='email', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confitmation_code = serializers.CharField()
