from django.db import models

from django.contrib.auth.models import AbstractUser

from .validators import username_validator
from foodgram.constants import LEN_254, LEN_150


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
        max_length=LEN_150,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=LEN_254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=LEN_150,
        unique=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=LEN_150,
        unique=False
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        null=True,
        default=None,
        verbose_name='Аватар'
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=len(max(USER_ROLES.values(), key=len)),
        choices=roles,
        default=USER,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

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
