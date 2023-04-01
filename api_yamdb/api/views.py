from rest_framework import status

from django.contrib.auth.tokens import default_token_generator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .serializers import User, AuthSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView

from reviews import models
from . import serializers


class AuthAPIView(APIView):
    """
     Регистрация и отправка кода подтверждения.
    """
    permission_classes = (AllowAny,)
    serializer_class = AuthSerializer

    def send_token(self, user):
        confirmation_code = default_token_generator.make_token(user)
        user.email_user('yamdb', f'confirmation_code: {confirmation_code}')

    def post(self, request):
        user = User.objects.filter(**request.data).first() or None
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_token(user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

