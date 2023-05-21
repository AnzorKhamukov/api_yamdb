from django_filters.filters import Filter
from reviews.models import Title
from django_filters.rest_framework.filterset import FilterSet


class TitleFilter(FilterSet):
    """Фильтрация произведений."""

    category = Filter(field_name='category__slug',)
    genre = Filter(field_name='genre__slug',)

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category',)
