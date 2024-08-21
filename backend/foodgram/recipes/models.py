from django.db import models

from users.models import User

from django.core.validators import (
    MinValueValidator, RegexValidator, FileExtensionValidator
)
from django.db.models import UniqueConstraint


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    measurement_unit = models.CharField(max_length=10)

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
    author = models.ForeignKey(
        User, related_name='author',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
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
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиентов'
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['recipe', 'ingredient'],
                             name='unique_recipe_ingredient')
        ]


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['recipe', 'tag'],
                             name='unique_recipe_tag')
        ]
