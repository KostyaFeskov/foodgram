from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import (
    TokenView, RegisterUserView, UserViewSet, UserLogoutView,
)

app_name = 'users'

# reviews_url = r'titles/(?P<title_id>\d+)/reviews'
# comments_url = rf'{reviews_url}/(?P<review_id>\d+)/comments'

# subscribe_url = rf'{reviews_url}/(?P<review_id>\d+)/comments'
users_urls = r'users'
# sibscription_urls = r'users/subscriptions/'

router = DefaultRouter()
# router.register(sibscription_urls, SubscribeViewSet, basename='subscriptions')
router.register(users_urls, UserViewSet, basename='users')


urlpatterns = [
    # re_path(
    #     r'users/(?P<id>)/subscribe/', SubscribeViewSet.as_view(
    #         {'post'}
    #     ), name='subscribe'
    # ),
    # path(
    #     'users/subscriptions/', SubscribeViewSet.as_view(
    #         {'get': 'list'}
    #     ), name='subscriptions'
    # ),
    path('', include(router.urls)),
    path('auth/token/login/', TokenView.as_view(), name='login'),
    path('auth/token/logout/', UserLogoutView.as_view(), name='logout'),
    path('auth/users/', RegisterUserView.as_view(), name='register')
]
