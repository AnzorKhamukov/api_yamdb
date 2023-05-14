from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    # name - required, string <= 256 characters
    name = models.CharField('Название категории', max_length=256)
    # slug - required, string <= 50 characters ^[-a-zA-Z0-9_]+$
    slug = models.SlugField('Slug категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    # name - required, string <= 256 characters
    name = models.CharField('Название жанра', max_length=256)
    # slug - required, string <= 50 characters ^[-a-zA-Z0-9_]+$
    slug = models.SlugField('Slug жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    # Получение списка всех произведений, к которым пишут отзывы.
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.CharField('Описание', max_length=256)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        # Доступ ко всем произведениям определенной категории
        related_name='titles',
        # Для произведения категория не обязательное поле
        blank=True,
        null=True,
        # При удалении категории, произведения сохранятся
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Категория, к которой будет относиться произведение',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    # Реализация связи жанра и произведения
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return f'{self.genre} {self.title}'
