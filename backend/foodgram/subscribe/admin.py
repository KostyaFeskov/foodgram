from django.contrib import admin

from .models import Subsribe

admin.site.empty_value_display = 'Пусто'


@admin.register(Subsribe)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subscription'
    )
    list_display_links = (
        'user',
        'subscription'
    )
    search_fields = (
        'user',
    )
