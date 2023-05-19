from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework.filterset import FilterSet
from django_filters.filters import Filter

from rest_framework import (viewsets, status, permissions, filters, mixins)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (
    AuthorOrStaffEditPermission, IsAdminOrReadOnly, IsAdmin)
from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Category, Genre, Review, Title, User
from .serializers import (
    CategorySerializer, GenreSerializer, UserSerializer,
    TitleSerializer, TitleReadSerializer, TitleCreateSerializer,
    GetTokenSerializer, SignUpSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    """Операции с комментариями к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrStaffEditPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Операции с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrStaffEditPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=serializer.validated_data['title']
        )


class ListCreateDestroyViewSet(
        mixins.CreateModelMixin, mixins.ListModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Миксин для Genre и Category"""
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    """Реализация методов GET, POST, DEL для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    """Реализация методов GET, POST, DEL для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleFilter(FilterSet):
    """Фильтрация произведений."""

    category = Filter(field_name='category__slug',)
    genre = Filter(field_name='genre__slug',)

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category',)


class TitleViewSet(viewsets.ModelViewSet):
    """Реализация над всеми операциями с произведениями."""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username',)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    permission_classes = [IsAdmin, ]
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
    message = 'Ваш уникальный код для получения токена.'
    email_from = 'yamdb.token@administration.com'
    try:
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
    except ValueError:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        message,
        confirmation_code,
        email_from,
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
