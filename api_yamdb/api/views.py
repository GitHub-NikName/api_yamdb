# from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


from reviews.models import Category, Genre, Title
from api.serializers import (CategoriesSerializer, GenreSerializer,
                             TitlesWriteSerializer, TitlesReadSerializer)
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
