from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.models import Q


from reviews.models import Category, Genre, Title, Review, Comment
from .utils import get_jwt_for_user


User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'


class TitlesWriteSerializer(serializers.ModelSerializer):
    """Произведения. Для записи"""
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
        fields = '__all__'


class TitlesReadSerializer(serializers.ModelSerializer):
    """Произведения. Для чтения"""
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True,
        default=None
    )
    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class SignUpSerializer(serializers.Serializer):
    """Сериализация регистрации и авторизации пользователя."""
    email = serializers.EmailField(
        max_length=254,
        required=True
    )
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
    """JWT токен"""
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
    """Для админа"""
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    """Профиль пользователея"""
    class Meta:
        fields = '__all__'
        model = User
        read_only_fields = ('role', )


class ReviewSerializer(serializers.ModelSerializer):
    """Отзывы"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        title_id = self.context['view'].kwargs['title_id']
        author = request.user
        if request.method == 'POST':
            if Review.objects.filter(title=title_id, author=author).exists():
                raise serializers.ValidationError(
                    'На каждое произведение можно оставить только один отзыв')
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Комментарии"""
    review = serializers.HiddenField(default=54)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
