from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Title(models.Model):
    pass


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
