from django.db import models


class Category(models.Model):
    # name - required, string <= 256 characters
    name = models.CharField('Название категории', max_length=256)
    # slug - required, string <= 50 characters ^[-a-zA-Z0-9_]+$
    slug = models.SlugField('Slug категории')


class Genre(models.Model):
    # name - required, string <= 256 characters
    name = models.CharField('Название жанра', max_length=256)
    # slug - required, string <= 50 characters ^[-a-zA-Z0-9_]+$
    slug = models.SlugField('Slug жанра')


class Title(models.Model):
    # Получение списка всех произведений, к которым пишут отзывы.
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.CharField('Описание')
    genre = models.SlugField('Жанр')
    category = models.SlugField('Категория')
