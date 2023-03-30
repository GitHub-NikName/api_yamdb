from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path('auth/signup/', views.AuthAPIView.as_view(), name='signup'),
#     path('auth/token/'),
#     path('auth/')
]
