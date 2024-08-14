from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import (
    RecipeViewSet, IngridientsViewSet, TagsViewSet
)

app_name = 'recipes'

# reviews_url = r'titles/(?P<title_id>\d+)/reviews'
# comments_url = rf'{reviews_url}/(?P<review_id>\d+)/comments'

router = DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingridients', IngridientsViewSet, basename='ingridients')
router.register('tags', TagsViewSet, basename='tags')
# router.register(reviews_url, ReviewViewSet, basename='reviews')
# router.register(comments_url, CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
]
