from rest_framework import status

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.urls import reverse
from django.shortcuts import get_object_or_404

from .models import (
    Ingredient,
    Recipe,
    Tag,
    ShoppingCart,
)

from .models import Favorite
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    ShoppingCartCreationSerializer,
    ShoppingCartDeleteSerializer,
    UserFavoriteCreationSerializer,
    UserFavoriteDeleteSerializer,
)

from urlshortener.serializers import UrlShortenerSerializer

from recipes.utils import create_xls_file


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create_favorite':
            return UserFavoriteCreationSerializer
        elif self.action == 'delete_favorite':
            return UserFavoriteDeleteSerializer
        elif self.action == 'get_short_link':
            return UrlShortenerSerializer
        elif self.action == 'add_in_shopping_cart':
            return ShoppingCartCreationSerializer
        elif self.action == 'delete_shopping_cart':
            return ShoppingCartDeleteSerializer
        return super().get_serializer_class()

    def _add_in_cart_or_in_favorite(self, request, pk):

        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance,
            data={'id': pk},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def _delete_from_shopping_cart_or_favorite(self, request, pk, model):
        recipe = get_object_or_404(Recipe, pk=pk)
        object = model.objects.filter(
            user=request.user,
            recipe=recipe
        )
        object.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        ['get'],
        detail=True,
        url_path='get-link'
    )
    def get_short_link(self, request, pk=None):

        self.get_object()
        url_original = request.META.get('HTTP_REFERER')
        if url_original is None:
            url_original = request.build_absolute_uri(
                reverse('api:recipe-detail', kwargs={'pk': pk})
            )
        serializer = self.get_serializer(
            data={'url_original': url_original},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        ['post'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path=r'(?P<pk>\d+)/shopping_cart'
    )
    def add_in_shopping_cart(self, request, pk):
        return self._add_in_cart_or_in_favorite(request, pk)

    @add_in_shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self._delete_from_shopping_cart_or_favorite(
            request, pk, ShoppingCart
        )

    @action(
        ['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):

        return create_xls_file(request)

    @action(
        ['post'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path=r'(?P<pk>\d+)/favorite'
    )
    def create_favorite(self, request, pk):
        return self._add_in_cart_or_in_favorite(request, pk)

    @create_favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self._delete_from_shopping_cart_or_favorite(
            request, pk, Favorite
        )

    def create(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response({
                'Не предоставлены учётные данные.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngridientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    http_method_names = ['get']


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    http_method_names = ['get']
