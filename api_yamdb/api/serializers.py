from rest_framework import serializers, validators
from rest_framework.validators import UniqueValidator

from .custom_serializers import CurrentReviewDefault, CurrentTitleDefault
from reviews.models import Comment, Review, Title, User, Category, Genre


class CommentSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializer(serializers.ModelSerializer):

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


class UserSerializer(serializers.ModelSerializer):
    """Cериалайзер кастомного пользователя."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер регистрации пользователей."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" недоступно'
            )
        if User.objects.filter(email=data['email'],
                               username=data['username']).exists():
            return data
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Этот email уже используется')
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Это имя уже занято.')

        return data


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериалайзер получения токена для пользователей."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
