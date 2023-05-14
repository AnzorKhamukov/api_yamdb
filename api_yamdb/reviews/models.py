from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    # name - required, string <= 256 characters
    name = models.CharField('Название категории', max_length=256)
    # slug - required, string <= 50 characters ^[-a-zA-Z0-9_]+$
    slug = models.SlugField('Slug категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    # name - required, string <= 256 characters
    name = models.CharField('Название жанра', max_length=256)
    # slug - required, string <= 50 characters ^[-a-zA-Z0-9_]+$
    slug = models.SlugField('Slug жанра')


class Title(models.Model):
    # Получение списка всех произведений, к которым пишут отзывы.
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.CharField('Описание', max_length=256)
    genre = models.SlugField('Жанр')
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
        help_text='Категория, к которой будет относиться произведение'
    )

    def __str__(self):
        return self.name
