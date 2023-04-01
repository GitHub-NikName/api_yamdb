import re
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


from reviews import models


User = get_user_model()


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
