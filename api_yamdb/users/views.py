from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from rest_framework import status, permissions, viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, action, permission_classes

from api.permissions import IsAdmin
from .serializers import (UserSerializer, GetTokenSerializer,
                          SignUpSerializer)
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username',)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    http_method_names = [
        'get', 'post', 'patch', 'delete'
    ]

    @action(methods=('get', 'patch'), url_path='me',
            detail=False, serializer_class=UserSerializer,
            permission_classes=(permissions.IsAuthenticated,))
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
@permission_classes([AllowAny])
def signup(request):
    """Регистрация пользователей + отправка письма на почту."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    try:
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
    except ValueError:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        settings.MESSAGE,
        confirmation_code,
        settings.EMAIL_FROM,
        [email],
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение уникального токена."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)

        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
