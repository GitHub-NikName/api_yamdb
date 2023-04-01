import re
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
        # if not re.match(r'^[\w.@+-]+$', username):
        #     raise serializers.ValidationError(
        #         'Используйте символы: [A-Za-z0-9_.@+-]'
        #     )
        return username

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.name
        # token['confirmation_code'] =

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
