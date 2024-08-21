from rest_framework import status

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

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

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
                'detail': 'Authentication credentials were not provided.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        serializer = RecipeSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngridientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
