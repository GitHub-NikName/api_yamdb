from rest_framework import serializers

from reviews import models


class AuthSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации и создания нового пользователя. """

    class Meta:
        model = models.User
        fields = ['email', 'username']

