import random
import string

from django.db import models


def get_hash():

    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(random.randint(6, 12))
    )


class LinkShortener(models.Model):

    url_hash = models.CharField(
        max_length=12,
        default=get_hash,
        unique=True
    )
    url_original = models.CharField(
        max_length=256,
    )

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    def __str__(self):
        return f'{self.url_original} -> {self.url_hash}'
