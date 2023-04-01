import re

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from reviews import models
from reviews.models import Category, Genre, Title

User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitlesWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name',
                  'year', 'description',
                  'genre', 'category')


class TitlesReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name',
                  'year', 'rating',
                  'description', 'genre',
                  'category')



class AuthSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации и авторизации пользователя. """

    class Meta:
        model = models.User
        fields = ('email', 'username')

    def validate_username(self, username: str):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Такое имя пользователя не доступно'
            )
        return username

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass
