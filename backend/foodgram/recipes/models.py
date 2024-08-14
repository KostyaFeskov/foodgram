from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    unit_of_measurement = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=256)
    text = models.TextField()
    owner = models.ForeignKey(
        User, related_name='cats',
        on_delete=models.CASCADE
    )
    ingridients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    cooking_time = models.IntegerField()
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingridient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingridient} {self.recipe}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingreidient} {self.recipe}'
