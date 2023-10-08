from django.db import models


class Coil(models.Model):
    """Модель рулона на складе."""

    length = models.DecimalField(
        'Длина рулона, м.',
        max_digits=20,
        decimal_places=3,
        help_text='Введите число',
    )
    weight = models.DecimalField(
        'Вес рулона, кг',
        max_digits=20,
        decimal_places=3,
        help_text='Введите число',
    )
    add_date = models.DateField(
        'Дата добавления рулона',
        auto_now_add=True
    )
    deletion_date = models.DateField(
        'Дата удаления рулона',
        blank=True,
        null=True,
    )

    class Meta:
        """Настройка отображения модели рулона."""

        ordering = ['add_date']
        verbose_name = 'Рулон'
        verbose_name_plural = 'Рулоны'

    def __str__(self):
        """Строковое представление модели."""

        return f'Рулон №{self.pk}'
