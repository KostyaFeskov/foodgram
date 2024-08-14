import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import (
    Ingredients,
    IngredientRecipe,
    Recipe,
    Tag,
    TagRecipe
)


class IngredientSerializer(serializers.ModelSerializer):
    ingridient_name = serializers.CharField(source='name')

    class Meta:
        model = Ingredients
        fields = ('id', 'ingridient_name')


class TagSerializer(serializers.ModelSerializer):
    tags = serializers.CharField(source='tag')

    class Meta:
        model = Tag
        fields = ('id', 'tag_name')    


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    ingridients = IngredientSerializer(required=True, many=True)
    image = Base64ImageField(required=True, allow_null=True)
    image_url = serializers.SerializerMethodField(
        'get_image_url',
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'ingridients',
            'owner', 'image', 'image_url', 'text',
            'cooking_time', 'tags'
        )
        read_only_fields = ('owner',)

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def create(self, validated_data):
        if 'ingridients' not in self.initial_data:
            recipe = Recipe.objects.create(**validated_data)
            return recipe
        if 'tags' not in self.initial_data:
            recipe = Recipe.objects.create(**validated_data)
            return recipe
        ingridients = validated_data.pop('ingridients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingridient in ingridients:
            current_ingridient, status = Ingredients.objects.get_or_create(
                **ingridient
            )
            IngredientRecipe.objects.create(
                ingridient=current_ingridient, recipe=recipe
            )
        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(
                **tag
            )
            TagRecipe.objects.create(
                tag=current_tag, recipe=recipe
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)

        if 'ingridients' not in validated_data:
            instance.save()
            return instance
        if 'tags' not in validated_data:
            instance.save()
            return instance

        ingridients_data = validated_data.pop('ingridients')
        lst = []
        for ingridient in ingridients_data:
            current_ingridient, status = Ingredients.objects.get_or_create(
                **ingridient
            )
            lst.append(current_ingridient)
        instance.ingridients.set(lst)

        tags_data = validated_data.pop('tags')
        lst = []
        for tag in tags_data:
            current_tag, status = Tag.objects.get_or_create(
                **tag
            )
            lst.append(current_tag)
        instance.tags.set(lst)

        instance.save()
        return instance