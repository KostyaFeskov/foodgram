import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

from foodgram import settings

DIR_DATA = settings.BASE_DIR / '../data'

class Command(BaseCommand):

    def handle(self, *args, **options):
        file_path = DIR_DATA / 'ingredients.json'
        file = open(file_path, 'r', encoding='UTF-8')
        data = json.load(file)
        for row in data:
            Ingredient.objects.get_or_create(
                **row
            )
        print('done')
