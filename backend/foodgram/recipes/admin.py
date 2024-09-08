from django.contrib import admin

from .models import IngredientRecipe, Recipe

admin.site.empty_value_display = 'Пусто'


class IngredientInline(admin.StackedInline):
    model = IngredientRecipe
    extra = 0
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        IngredientInline,
    )
    filter_horizontal = ('tags',)
    list_display = (
        'name',
        'author',
        'cooking_time',
    )
    list_display_links = (
        'name',
        'author',
    )
    list_filter = (
        'tags',
    )
    search_fields = (
        'name',
        'author',
    )