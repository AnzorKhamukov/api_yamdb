from rest_framework import serializers, validators

from reviews.models import Comment, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
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
        slug_field='title',
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
