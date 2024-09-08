from django.db import models

from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError

User = get_user_model()


class Subsribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь'
    )
    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Подписка'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
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
