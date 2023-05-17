from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, action, permission_classes
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
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = [AllowAny, ]

    @action(methods=(['GET', 'PATCH']), detail=False)
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
    message = 'Ваш уникальный токен для регистрации'
    email_from = 'yamdb.token@administration.com'

    try:
        user, created = User.objects.get_or_create(
            username=username,
            email=email
            )
        confirmation_code = default_token_generator.make_token(user)

        send_mail(message,
                  confirmation_code,
                  email_from,
                  [email],
                  fail_silently=False
                  )

        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError:
        raise serializers.ValidationError(
            'На данный email или имя пользователя уже зарегистрировались'
        )


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
