from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import (
    UserViewSet
)

app_name = 'users'

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
