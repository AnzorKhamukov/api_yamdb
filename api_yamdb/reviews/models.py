from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Кастомная модель пользователя."""
    USER_TYPE = (
        ('user', 'пользователь'),
        ('moderator', 'модератор'),
        ('admin', 'администратор'),
    )

    email = models.EmailField(
        max_length=254,
        verbose_name='Почта пользователя'
    )
    bio = models.TextField(
        max_length=200,
        null=True,
        verbose_name='О себе'
    )
    role = models.CharField(
        max_length=12,
        choices=USER_TYPE,
        default='user',
        verbose_name='Тип пользователя'
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)

    @property
    def is_user(self):
        """Проверка на наличие прав авторизированного пользователя."""
        return self.role == 'user'

    @property
    def is_admin(self):
        """Проверка на наличие прав администратора."""
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка на наличие прав модератора."""
        return self.role == 'moderator'


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField(
        'Slug категории',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField(
        'Slug жанра',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    # Получение списка всех произведений, к которым пишут отзывы.
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField(
        'Описание', max_length=256, blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(
        Category,
        # Доступ ко всем произведениям определенной категории
        related_name='titles',
        # # Для произведения категория не обязательное поле
        blank=True,
        null=True,
        # При удалении категории, произведения сохранятся
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Категория, к которой будет относиться произведение',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField('Содержание отзыва')
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True, db_index=True
    )
    # При удалении пользователя отзыв удаляется
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
    )
    # При удалении произведения отзыв удаляется
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
    )
    # Оценка в диапазоне от одного до десяти (целое число)
    score = models.IntegerField(
        'Оценка произведения',
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ],
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        # На одно произведение пользователь может оставить только один отзыв.
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField('Содержание комментария')
    pub_date = models.DateTimeField(
        'Дата публикации комментария', auto_now_add=True, db_index=True
    )
    # При удалении пользователя все его комментарии удаляются.
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    # При удалении отзыва все комментарии удаляются.
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
