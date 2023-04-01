
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (CategoriesViewSet, GenreViewSet, TitlesViewSet, AuthAPIView)
from .serializers import TokenAuthSerializer

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', AuthAPIView.as_view(), name='signup'),
    path('auth/token/',
         TokenObtainPairView.as_view(serializer_class=TokenAuthSerializer),
         name='token_obtain_pair'),
]

