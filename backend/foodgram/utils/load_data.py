# from django.core.management.base import BaseCommand, CommandError
# from django.shortcuts import get_object_or_404
# from django.apps import apps
# from foodgram import settings
# import csv


# FOREIGNKEY_FIELDS = ('name', 'unit_of_measurement',)
# DIR_DATA = settings.BASE_DIR / 'data'
# FILES = (
#     "ingredients.csv",
# )


# class Command(BaseCommand):
#     help = """Импортирует данные из csv-файла в модель.
#     Пример: python manage.py load_data
#     Файлы берутся из директории /data/"""

#     def get_model_name(self, file_name):
#         """Возвращает имя модели по имени файла."""
#         model_name = file_name.rstrip('.csv')
#         if '_' in model_name:
#             model_name = model_name.replace('_', '')
#         return model_name

#     def get_model(self, model_name):
#         """Возвращает модель по полю из файла."""
#         if model_name == 'ingredients':
#             Model = apps.get_model('reviews', 'user')
#         else:
#             Model = apps.get_model('reviews', model_name)
#         if not Model:
#             raise CommandError(f'Модель {Model} не существует.')
#         return Model

#     def load_data(self, file_name):
#         """Загружает данные из файла в базу."""
#         file_path = DIR_DATA / file_name
#         model_name = self.get_model_name(file_name)
#         Model = self.get_model(model_name)
#         try:
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 self. stdout.write(f'Чтение файла {file_name}')
#                 reader = csv.DictReader(file)
#                 for row in reader:
#                     Obj = Model()
#                     for i, field in enumerate(row.values()):
#                         if reader.fieldnames[i] in FOREIGNKEY_FIELDS:
#                             model = self.get_model(reader.fieldnames[i])
#                             obj = get_object_or_404(model, id=field)
#                             setattr(Obj, reader.fieldnames[i], obj)
#                         else:
#                             setattr(Obj, reader.fieldnames[i], field)
#                     Obj.save()
#         except Exception as e:
#             raise CommandError(f'Ошибка при чтение файла {file_name}: {e}')
#         else:
#             self.stdout.write(self.style.SUCCESS(
#                 f'Данные из файла {file_name} успешно внесены в базу данных.'
#             ))

#     def handle(self, *args, **options):
#         for file_name in FILES:
#             self.load_data(file_name)
