from rest_framework import serializers, validators

from .custom_serializers import CurrentReviewDefault, CurrentTitleDefault
from reviews.models import Comment, Review, Title, Category, Genre
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    review = serializers.SlugRelatedField(
        read_only=False,
        slug_field='text',
        default=CurrentReviewDefault(),
        queryset=Review.objects.all()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'pub_date', 'author', 'review',)
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор рецензий."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    title = serializers.SlugRelatedField(
        read_only=False,
        slug_field='name',
        default=CurrentTitleDefault(),
        queryset=Title.objects.all()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'pub_date', 'author', 'title', 'score',)
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title',),
                message='Отзыв уже есть',
            ),
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для типа Title."""
    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    '''Получение информации о произведении'''
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    '''Добавление произведения'''
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
