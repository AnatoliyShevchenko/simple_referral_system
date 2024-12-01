# Generated by Django 5.1.3 on 2024-11-30 07:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(blank=True, max_length=256, null=True, verbose_name='пароль')),
                ('invite_code', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('activated_invite_code', models.CharField(blank=True, max_length=6, null=True)),
                ('auth_code', models.CharField(blank=True, max_length=4, null=True)),
                ('auth_code_expires', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='активный')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='администратор')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('invited_users', models.ManyToManyField(related_name='invited_by', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
                'ordering': ('-id',),
            },
        ),
    ]
