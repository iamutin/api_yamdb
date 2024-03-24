from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    USER_ROLES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    )

    email = models.EmailField(
        'Электронная почта', unique=True, max_length=254
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', choices=USER_ROLES, default=USER, max_length=15
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
