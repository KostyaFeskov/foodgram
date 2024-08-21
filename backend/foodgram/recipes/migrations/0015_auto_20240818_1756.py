# Generated by Django 3.2.3 on 2024-08-18 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0014_auto_20240818_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='owner',
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='users.user'),
            preserve_default=False,
        ),
    ]
