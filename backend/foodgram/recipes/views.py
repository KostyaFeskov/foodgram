import xlwt

from rest_framework import status

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.urls import reverse
from django.db.models import Sum


from .models import (
    Ingredient,
    Recipe,
    Tag,
    ShoppingCart,
    IngredientRecipe
)

from favorite.models import Favorite
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    ShoppingCartCreationSerializer,
    ShoppingCartDeleteSerializer,
)

from favorite.serializers import (
    UserFavoriteCreationSerializer,
    UserFavoriteDeleteSerializer,
)
from urlshortener.serializers import UrlShortenerSerializer


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
        elif self.action == 'is_in_shopping_cart':
            return ShoppingCartCreationSerializer
        elif self.action == 'delete_shopping_cart':
            return ShoppingCartDeleteSerializer
        return super().get_serializer_class()

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
    def is_in_shopping_cart(self, request, pk):

        buy_recipe = self.get_object()
        serializer = self.get_serializer(
            instance=buy_recipe,
            data={'id': pk},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        ShoppingCart.objects.create(
            user=request.user,
            recipe=buy_recipe
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @is_in_shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):

        buy_recipe = self.get_object()
        serializer = self.get_serializer(
            instance=buy_recipe,
            data={'id': pk},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        ShoppingCart.objects.filter(
            user=request.user,
            recipe=buy_recipe
        ).delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        ['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):

        ingredient_list = IngredientRecipe.objects.filter(
            recipe__shopping_cart_recipe__user=request.user
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(Sum('amount'))

        response = HttpResponse(
            content_type='application/vnd.ms-excel',
            headers={
                'Content-Disposition':
                'attachment; filename="to_buy_list.xls"'
            },
        )
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [
            'Название ингредиента',
            'Единица измерения',
            'Количество',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()

        for row in ingredient_list:
            row_num = row_num + 1
            ws.write(row_num, 0, row[0], font_style)
            ws.write(row_num, 1, row[1], font_style)
            ws.write(row_num, 2, row[2], font_style)

        wb.save(response)
        return response

    @action(
        ['post'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path=r'(?P<pk>\d+)/favorite'
    )
    def create_favorite(self, request, pk):

        favorite_recipe = self.get_object()
        serializer = self.get_serializer(
            instance=favorite_recipe,
            data={'id': pk},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Favorite.objects.create(
            user=request.user,
            favorite=favorite_recipe
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @create_favorite.mapping.delete
    def delete_favorite(self, request, pk):

        favorite_recipe = self.get_object()
        serializer = self.get_serializer(
            instance=favorite_recipe,
            data={'id': pk},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Favorite.objects.filter(
            user=request.user,
            favorite=favorite_recipe
        ).delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
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
