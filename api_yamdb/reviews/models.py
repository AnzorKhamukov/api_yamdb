from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Кастомная модель пользователя."""
    USER_TYPE = (
        ('user', 'пользователь'),
        ('moderator', 'модератор'),
        ('admin', 'администратор'),
    )
    username = models.CharField(
        max_length=155,
        verbose_name='Имя пользователя',
        unique=True,
        blank=False
    )
    email = models.EmailField(
        max_length=155,
        unique=True,
        verbose_name='Почта пользователя'
        )
    bio = models.TextField(
        max_length=200,
        null=True,
        verbose_name='О себе'
        )
    role = models.CharField(
        max_length=100,
        choices=USER_TYPE,
        default='user',
        verbose_name='Тип пользователя'
        )

    @property
    def is_user(self):
        """Проверка на наличие прав авторизированного пользователя."""
        return self.user_type == 'user'

    @property
    def is_admin(self):
        """Проверка на наличие прав администратора."""
        return self.user_type == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка на наличие прав модератора."""
        return self.user_type == 'moderator'

    @property
    def __str__(self):
        return self.username
