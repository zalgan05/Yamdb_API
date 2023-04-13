from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )  # порядок вывода, как в redoc
        model = Title


class GenreSerializer:
    class Meta:
        fields = "__all__"
        model = Genre


class CategorySerializer:
    class Meta:
        fields = "__all__"
        model = Category
