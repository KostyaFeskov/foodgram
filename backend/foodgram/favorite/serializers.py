import base64

from rest_framework import serializers

from recipes.models import Recipe
from recipes.serializers import RecipeShortSerializer
from favorite.models import Favorite

class UserFavoriteActionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id',)

    def to_representation(self, instance):
        serializer = UserFavoriteSerializer(
            instance,
            context={'request': self.context['request']}
        )
        return serializer.data


class UserFavoriteCreationSerializer(UserFavoriteActionSerializer):
    def validate_id(self, request):
        if Favorite.objects.filter(
            user=self.context['request'].user,
            favorite=request
        ).exists():
            raise serializers.ValidationError(
                f'Рецепт ID №{request} уже в избранном.'
            )
        return request


class UserFavoriteDeleteSerializer(UserFavoriteActionSerializer):
    def validate_id(self, request):
        if not Favorite.objects.filter(
            user=self.context['request'].user,
            favorite=request
        ).exists():
            raise serializers.ValidationError(
                f'Рецепта ID №{request} нет в избранном.'
            )
        return request


class UserFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit'
        )
        queryset = Recipe.objects.filter(author=obj)
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        serializer = RecipeShortSerializer(
            queryset,
            context={'request': self.context['request']},
            many=True
        )
        return serializer.data
    