from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.valitadors import validate_year
from .managers import UserManager


CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
)


class Category(models.Model):
    name = models.TextField(max_length=256,
                            verbose_name='Название категории')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def str(self):
        return self.slug


class Genre(models.Model):
    name = models.TextField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def str(self):
        return self.slug


class Title(models.Model):
    name = models.TextField(max_length=256,
                            verbose_name='Название')
    year = models.PositiveIntegerField(db_index=True,
                                       verbose_name='Год',
                                       validators=(validate_year,))
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   verbose_name='Жанр')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def str(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              verbose_name='Жанр')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='Название')

    def str(self):
        return f'{self.genre} {self.title}'


class User(AbstractUser):
    email = models.EmailField(
        'email',
        unique=True,
        db_index=True,
        error_messages={
            'unique':
                "Пользователь с таким адресом электронной почты уже существует"
        },
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        max_length=500
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=16,
        choices=CHOICES,
        default='user'
    )

    objects = UserManager()

    def __str__(self):
        return self.username

