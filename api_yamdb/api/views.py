from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework.filterset import FilterSet
from django_filters.filters import Filter

from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination

from .permissions import AuthorOrStaffEditPermission, IsAdminOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Category, Genre, Review, Title
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleSerializer, TitleReadSerializer, TitleCreateSerializer,)


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
