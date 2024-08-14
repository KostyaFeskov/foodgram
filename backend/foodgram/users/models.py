from django.db import models
from django.utils import timezone
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import username_validator

USER_ROLES = {
    'user': 'user',
    'moderator': 'moderator',
    'admin': 'admin',
}
USER = USER_ROLES['user']
MODERATOR = USER_ROLES['moderator']
ADMIN = USER_ROLES['admin']


class User(AbstractUser):
    """Модель пользователя."""

    roles = list(USER_ROLES.items())

    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='first_name',
        max_length=150,
        unique=False
    )
    last_name = models.CharField(
        verbose_name='last_name',
        max_length=150,
        unique=False
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        null=True,
        default=None
    )
    is_subscribed = models.BooleanField(
        default=False
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=len(max(USER_ROLES.values(), key=len)),
        choices=roles,
        default=USER,
    )

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
