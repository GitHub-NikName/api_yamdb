from rest_framework import status

from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import mixins, viewsets, views
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title
from api.serializers import (CategoriesSerializer, GenreSerializer,
                             TitlesWriteSerializer, TitlesReadSerializer,
                             AuthSerializer, User)

from api.filters import TitlesFilter


class CategoriesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    # permission_classes =  # добавить пермишен


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    # permission_classes =  # добавить пермишен


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    # permission_classes =  # добавить пермишен

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return TitlesWriteSerializer

        return TitlesReadSerializer


class AuthAPIView(views.APIView):
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


