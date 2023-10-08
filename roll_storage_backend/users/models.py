from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        'Имя пользователя',
        max_length=128,
        unique=True,
        null=False,
        blank=False,
        help_text='Здесь должен быть логин для входа'
    )
    first_name = models.CharField(
        'Имя',
        max_length=128,
        null=True,
        blank=True,
        help_text='Например "Владимир"'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=128,
        null=True,
        blank=True,
        help_text='Например "Петров"'
    )

    USERNAME_FIELD = 'username'

    class Meta:
        """Настройки отображения модели."""

        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковое представление модели."""

        return self.username
