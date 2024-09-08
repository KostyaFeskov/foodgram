from recipes.models import Ingredient
from recipes.models import Tag
from .models import IngredientRecipe, Recipe


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
