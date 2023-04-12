from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Genre, Title, Category


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


class GenreSerializer():
    pass


class CategorySerializer():
    pass
