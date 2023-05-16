from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from reviews.models import User
from .serializers import UserSerializer, SignUpSerializer, GetTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    search_fields = 'username',
    lookup_field = 'username'
    permission_classes = [AllowAny, ]

    @action(methods=(['GET', 'PATCH']),)
    def me(self, request):
        """Получение данных своей учётной записи."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    """Регистрация пользователей + отправка письма на почту."""
    serializer = SignUpSerializer
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['user']
    email = serializer.validated_data['email']
    user = User.objects.create(username=username, email=email)
    message = 'Ваш уникальный токен для регистрации'
    email_from = 'yamdb.token@administration.com'
    token = default_token_generator.make_token(user)

    try:
        send_mail(message, token, [email], email_from, fail_silently=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError:
        raise serializers.ValidationError(
            'На данный email или имя пользователя уже зарегистрировались'
        )


@api_view(['POST'])
def get_token(request):
    """Получение уникального токена."""
    serializer = GetTokenSerializer
    serializer.is_valid()
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)

    if default_token_generator.chek_token(user, confirmation_code):
        token = AccessToken.for_user(user)

        return Response({'token': token}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
