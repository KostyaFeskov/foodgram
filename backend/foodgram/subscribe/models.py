from django.db import models

from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError

User = get_user_model()

class Subsribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'subscription'),
                name='unique_subscribtion'
            ),)
        
    def clean(self) -> None:
        if self.user == self.subscription:
            raise ValidationError(
                {
                    'subscribe_target': 'Нельзя подписаться на себя.'
                }
            )

