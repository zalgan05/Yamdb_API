from reviews.models import Review
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    """Преобразовывает объекты модели Review"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('author', 'title',)
