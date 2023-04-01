from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title

User = get_user_model()


def get_jwt_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }


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
        model = User
        fields = ('email', 'username')

    def validate_username(self, username: str):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Такое имя пользователя не доступно'
            )
        return username

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        return instance


class TokenAuthSerializer(serializers.Serializer):
    username = serializers.RegexField(r'^[\w.@+-]+$', max_length=150)
    confirmation_code = serializers.CharField(max_length=100)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
                user, data['confirmation_code']
        ):
            raise serializers.ValidationError('Код подтверждения не верный')
        return get_jwt_for_user(user)
