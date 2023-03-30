from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
)


class UserManager(BaseUserManager):
    """
    Менеджер для модели пользователя.
    """

    def create_user(self, username, email):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.save()
        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


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
