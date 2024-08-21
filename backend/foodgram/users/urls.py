from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    TokenView, RegisterUserView, UserViewSet, UserLogoutView,
    SubscribeViewSet
)

app_name = 'users'

# reviews_url = r'titles/(?P<title_id>\d+)/reviews'
# comments_url = rf'{reviews_url}/(?P<review_id>\d+)/comments'

# subscribe_url = rf'{reviews_url}/(?P<review_id>\d+)/comments'

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('users/subscriptions', SubscribeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', TokenView.as_view(), name='login'),
    path('auth/token/logout/', UserLogoutView.as_view(), name='logout'),
    path('auth/users/', RegisterUserView.as_view(), name='register')
]
