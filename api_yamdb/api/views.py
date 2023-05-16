from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


from reviews.models import User
from .serializers import UserSerializer, SignUpSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    search_fields = 'username',
    lookup_field = 'username'
    permission_classes = [AllowAny, ]


@api_view(['POST'])
def signup(request):
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

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValueError:
        raise serializers.ValidationError(
            'На данный email или имя пользователя уже зарегистрировались'
        )
