import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        file = open('../../data/ingredients.json', 'r', encoding='UTF-8')
        data = json.load(file)
        for row in data:
            Ingredient.objects.get_or_create(
                **row
            )
        print('done')
