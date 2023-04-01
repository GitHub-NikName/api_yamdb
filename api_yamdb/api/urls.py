from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views


urlpatterns = [
    path('auth/signup/', views.AuthAPIView.as_view(), name='signup'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('auth/')
]
