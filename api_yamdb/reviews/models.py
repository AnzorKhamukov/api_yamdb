from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField(
        'Slug категории',
        max_length=256,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField('Название жанра', max_length=50)
    slug = models.SlugField(
        'Slug жанра',
        max_length=256,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    # Получение списка всех произведений, к которым пишут отзывы.
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField(
        'Описание', max_length=256, null=True)
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
    """Модель рецензий."""
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
    score = models.PositiveSmallIntegerField(
        'Оценка произведения',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ],
    )

    class Meta:
        ordering = ('pub_date',)
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
    """Модель комментариев к рецензии."""
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
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
