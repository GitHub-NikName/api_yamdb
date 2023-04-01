from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, GenreViewSet, TitlesViewSet)

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')
