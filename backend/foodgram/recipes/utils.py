import base64
import xlwt

from rest_framework import serializers, status

from rest_framework.response import Response

from django.core.files.base import ContentFile

from django.http import HttpResponse
from django.db.models import Sum

from recipes.models import Ingredient
from recipes.models import Tag
from .models import IngredientRecipe, Recipe, ShoppingCart


def create_ingredient(
        recipe: Recipe, ingredients_data: list[dict[str, int]]
):

    if not recipe or not ingredients_data:
        return
    for ingredient in ingredients_data:
        IngredientRecipe.objects.create(
            ingredient=Ingredient.objects.get(
                pk=ingredient['id']
            ),
            recipe=recipe,
            amount=ingredient['amount']
        )


def add_tags(recipe: Recipe, tags_data: list[int]):

    if not recipe or not tags_data:
        return
    for tag_id in tags_data:
        recipe.tags.add(
            Tag.objects.get(pk=tag_id)
        )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


def create_xls_file(request):
    ingredient_list = IngredientRecipe.objects.filter(
        recipe__shopping_cart_recipe__user=request.user
    ).values_list(
        'ingredient__name',
        'ingredient__measurement_unit',
    ).annotate(sum_of_amount=Sum('amount'))

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
