from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.models import Q


from reviews.models import Category, Genre, Title
from .utils import get_jwt_for_user


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


class SignUpSerializer(serializers.Serializer):
    """Сериализация регистрации пользователя."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    def validate(self, attrs):
        if User.objects.filter(Q(username=attrs['username'])
                               & Q(email=attrs['email'])):
            return attrs
        if User.objects.filter(Q(username=attrs['username'])
                               | Q(email=attrs['email'])):
            raise serializers.ValidationError(
                {'Пользователь с такими данными уже есть'}
            )
        return attrs

    def validate_username(self, username: str):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Такое имя пользователя не доступно'
            )
        return username


class TokenAuthSerializer(serializers.Serializer):
    username = serializers.RegexField(r'^[\w.@+-]+$', max_length=150)
    confirmation_code = serializers.CharField(max_length=100)

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        if not default_token_generator.check_token(
                user, data.get('confirmation_code')
        ):
            raise serializers.ValidationError('Код подтверждения не верный')
        return get_jwt_for_user(user)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role', )
