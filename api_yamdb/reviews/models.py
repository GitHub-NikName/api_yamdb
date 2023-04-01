from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
)


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
