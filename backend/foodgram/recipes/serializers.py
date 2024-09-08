import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import (
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
    ShoppingCart
)
from favorite.models import Favorite
from users.serializers import UserMeSerializer
from .utils import create_ingredient, add_tags


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientRecipeSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeShortSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

    def get_image(self, obj):
        return self.context.get('request').build_absolute_uri(obj.image.url)


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserMeSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorite',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        recipe_ingredients = IngredientRecipe.objects.filter(recipe=obj)
        result = []
        for recipe_ingredient in recipe_ingredients:
            ingredient_data = IngredientSerializer(
                recipe_ingredient.ingredient
            ).data
            ingredient_data['amount'] = recipe_ingredient.amount
            result.append(ingredient_data)
        return result

    def get_is_favorite(self, obj):
        return (
            self.context['request'].user.is_authenticated
            and Favorite.objects.filter(
                user=self.context['request'].user,
                favorite=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.context['request'].user.is_authenticated
            and ShoppingCart.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(many=True)
    tags = serializers.ListField(child=serializers.IntegerField())
    cooking_time = serializers.IntegerField()
    name = serializers.CharField(max_length=258)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate_name(self, value):
        if Recipe.objects.filter(
            name=value,
            author=self.context['request'].user
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Вы уже создавали рецепт с таким названием.'
            )
        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'Заполните поле ингредиентов.'
            )
        ingredient_ids = []
        for ingredient in value:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше 0.'
                )

            ingredient_id = ingredient['id']
            if ingredient_id in ingredient_ids:
                raise serializers.ValidationError(
                    'Уберите повторяющиеся ингредиенты.'
                )
            ingredient_ids.append(ingredient_id)

            if not Ingredient.objects.filter(pk=ingredient_id).exists():
                raise serializers.ValidationError(
                    f'Ингредиента с id {ingredient_id} не существует.'
                )
        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                'Заполните поле тэгов.'
            )

        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                'Уберите повторяющиеся тэги.'
            )

        for tag in value:
            if not Tag.objects.filter(pk=tag).exists():
                raise serializers.ValidationError(
                    f'Тэга с id {tag} не существует.'
                )
        return value

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Время должно быть больше 0.'
            )
        return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        create_ingredient(recipe, ingredients_data)
        add_tags(recipe, tags_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instance.ingredients.clear()
        create_ingredient(instance, ingredients_data)

        tags_data = validated_data.pop('tags')
        instance.tags.clear()
        add_tags(instance, tags_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance,
            context={'request': self.context['request']}
        )
        return serializer.data


class ShoppingCartActionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id',)

    def to_representation(self, instance):
        serializer = RecipeShortSerializer(
            instance,
            context={'request': self.context['request']}
        )
        return serializer.data


class ShoppingCartCreationSerializer(ShoppingCartActionSerializer):
    def validate_id(self, request):
        if ShoppingCart.objects.filter(
            user=self.context['request'].user,
            recipe=request
        ).exists():
            raise serializers.ValidationError(
                f'Рецепт ID №{request} уже в списке покупок.'
            )
        return request


class ShoppingCartDeleteSerializer(ShoppingCartActionSerializer):
    def validate_id(self, request):
        if not ShoppingCart.objects.filter(
            user=self.context['request'].user,
            recipe=request
        ).exists():
            raise serializers.ValidationError(
                f'Рецепта ID №{request} нет в списке покупок.'
            )
        return request
