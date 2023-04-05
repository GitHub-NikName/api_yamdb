from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (CategoriesViewSet, GenreViewSet, TitlesViewSet,
                    UserViewSet, signup, ReviewVieSet, CommentViewSet)
from .serializers import TokenAuthSerializer

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewVieSet,
                   basename='review')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)


urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/',
         TokenObtainPairView.as_view(serializer_class=TokenAuthSerializer),
         name='token_obtain_pair'),
]
