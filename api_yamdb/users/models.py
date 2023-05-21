from django.db import models

from django.contrib.auth.models import AbstractUser

user = 'user'
moderator = 'moderator'
admin = 'admin'


class User(AbstractUser):
    """Кастомная модель пользователя."""

    USER_TYPE = (
        (user, 'пользователь'),
        (moderator, 'модератор'),
        (admin, 'администратор'),
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
        default=user,
        verbose_name='Тип пользователя'
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)

    @property
    def is_user(self):
        """Проверка на наличие прав авторизированного пользователя."""
        return self.role == user

    @property
    def is_admin(self):
        """Проверка на наличие прав администратора."""
        return self.role == admin or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка на наличие прав модератора."""
        return self.role == moderator
