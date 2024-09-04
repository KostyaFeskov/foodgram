from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import (
    RecipeViewSet, IngridientsViewSet, TagsViewSet
)

app_name = 'recipes'

router = DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngridientsViewSet, basename='ingridients')
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]
