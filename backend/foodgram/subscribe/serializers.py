from rest_framework import serializers

from recipes.models import Recipe
from recipes.serializers import RecipeShortSerializer
from subscribe.models import Subsribe

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSubscriptionActionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id',)

    def to_representation(self, instance):
        serializer = UserSubscriptionSerializer(
            instance,
            context={'request': self.context['request']}
        )
        return serializer.data


class UserSubscriptionCreationSerializer(UserSubscriptionActionSerializer):
    def validate_id(self, request):
        if self.context['request'].user.id == request:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя.'
            )
        if Subsribe.objects.filter(
            user=self.context['request'].user,
            subscription=request
        ).exists():
            raise serializers.ValidationError(
                f'Вы уже подписаны на пользователя ID №{request}.'
            )
        return request


class UserSubscriptionDeleteSerializer(UserSubscriptionActionSerializer):
    def validate_id(self, request):
        if not Subsribe.objects.filter(
            user=self.context['request'].user,
            subscription=request
        ).exists():
            raise serializers.ValidationError(
                f'Нет подписки на пользователя ID №{request}.'
            )
        return request


class UserSubscriptionSerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
            'avatar',
            'recipes',
            'recipes_count'
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