from django.db import models

from recipes.models import Recipe

from django.contrib.auth import get_user_model

User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )
    favorite = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'favorite'),
                name='unique_favorite'
            ),)

