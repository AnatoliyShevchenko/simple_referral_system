# Generated by Django 5.1.3 on 2024-11-30 13:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='activated_invite_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='invited_users',
        ),
        migrations.AddField(
            model_name='user',
            name='inviter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invited_users', to=settings.AUTH_USER_MODEL, verbose_name='Пригласивший пользователь'),
        ),
        migrations.AlterField(
            model_name='user',
            name='auth_code',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='код авторизации'),
        ),
        migrations.AlterField(
            model_name='user',
            name='auth_code_expires',
            field=models.DateTimeField(blank=True, null=True, verbose_name='время действия кода активации'),
        ),
        migrations.AlterField(
            model_name='user',
            name='invite_code',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True, verbose_name='Код приглашения'),
        ),
    ]
