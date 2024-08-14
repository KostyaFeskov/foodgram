from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Ingredient, Recipe, Tag
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IngridientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
