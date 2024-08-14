
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import (
    TokenView, RegisterUserView, UserViewSet
)

# router = DefaultRouter()
# router.register('users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    # path('api/', include(router.urls)),
    path('api/', include('recipes.urls')),
    # path('api/auth/token/login/', TokenView.as_view(), name='token'),
    # path('api/auth/signup/', RegisterUserView.as_view(), name='register')

]
