from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination


from reviews.models import Category, Genre, Title
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleSerializer, TitleReadSerializer, TitleCreateSerializer)
from .permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
        mixins.CreateModelMixin, mixins.ListModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Миксин для Genre и Category"""
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer
