# Django
from django.contrib.auth.models import \
    AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Python
import random
import string
from datetime import timedelta

# Third-Party
from loguru import logger


class UserManager(BaseUserManager):
    def create_user(self, phone: str) -> "User":
        if not phone:
            raise ValueError("The phone field must be set")
        user: "User" = self.model(phone=phone)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone: str, password: str) -> "User":
        if not phone or not password:
            raise ValueError(
                "Fields 'Phone' and 'Password' are required!"
            )
        user: User = self.model(phone=phone)
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(
        verbose_name="пароль", max_length=256, blank=True, null=True
    )
    invite_code = models.CharField(
        max_length=6, unique=True, blank=True, 
        null=True, verbose_name="Код приглашения"
    )
    inviter = models.ForeignKey(
        "self", on_delete=models.SET_NULL, 
        blank=True, null=True, related_name="invited_users", 
        verbose_name="Пригласивший пользователь"
    )
    auth_code = models.CharField(
        max_length=4, blank=True, null=True, 
        verbose_name="код авторизации"
    )
    auth_code_expires = models.DateTimeField(
        blank=True, null=True, 
        verbose_name="время действия кода активации"
    )
    is_active = models.BooleanField(
        verbose_name="активный", default=False
    )
    is_staff = models.BooleanField(
        verbose_name="менеджер", default=False
    )
    is_superuser = models.BooleanField(
        verbose_name="администратор", default=False
    )

    objects = UserManager()

    USERNAME_FIELD = "phone"

    class Meta:
        ordering = ('-id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    @staticmethod
    def generate_auth_code() -> str:
        while True:
            code = "".join(random.choices(string.digits, k=4))
            if not User.objects.filter(auth_code=code).exists():
                return code

    def set_auth_code(self) -> str:
        """
        Генерируем и сохраняем новый код авторизации.
        Будет действителен всего 2 минуты.
        """
        self.auth_code = self.generate_auth_code()
        self.auth_code_expires = timezone.now() + timedelta(minutes=2)
        self.save()
        return self.auth_code
            
    @staticmethod
    def generate_invite_code() -> str:
        while True:
            code = "".join(random.choices(
                string.ascii_letters + string.digits, k=6
            ))
            if not User.objects.filter(invite_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        """
        Генерируем код приглашения только при создании пользователя.
        """
        if self.pk:
            super().save(*args, **kwargs)
            return
        self.invite_code = self.generate_invite_code()
        try:
            self.full_clean()
            super().save(*args, **kwargs)
            logger.info(f"Client with phone number {self.phone} has been registered")
        except Exception as e:
            logger.error(f"Cannot register Client with phone number {self.phone}. ERROR: {e}")
            raise 

    def __str__(self) -> str:
        return f"{self.phone}"
