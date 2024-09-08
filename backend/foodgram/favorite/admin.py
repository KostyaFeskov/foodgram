from django.contrib import admin

from .models import Favorite

admin.site.empty_value_display = 'Пусто'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'favorite'
    )
    list_display_links = (
        'user',
        'favorite',
    )
    search_fields = (
        'user',
    )
