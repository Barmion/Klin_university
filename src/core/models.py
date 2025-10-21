from django.contrib.auth import get_user_model
from django.db import models

from core.constants import MAX_LENGTH

User = get_user_model()


class Position(models.Model):
    name = models.CharField(
        verbose_name='Название должности',
        max_length=MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'должность'
        verbose_name_plural = 'Должности'
        ordering = ['name',]

    def __str__(self):
        return self.name


class Worker(models.Model):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LENGTH,
    )
    middle_name = models.CharField(
        verbose_name='Отчество',
        max_length=MAX_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LENGTH,
    )
    email = models.EmailField(
        verbose_name='адрес электронной почты',
        unique=True,
        blank=False,
        null=False,
    )
    position = models.ForeignKey(
        Position,
        verbose_name='Должность',
        on_delete=models.PROTECT,
        related_name='workers',
    )
    is_active = models.BooleanField(
        verbose_name='Активность',
        default=True,
    )
    hired_date = models.DateTimeField(
        verbose_name='Дата приема на работу',
        auto_now_add=True,
    )
    created_by = models.ForeignKey(
        User,
        verbose_name='Кем создано',
        on_delete=models.PROTECT,
        related_name='created_workers',
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
    )

    def get_full_name(self):
        return (
            f'{self.last_name} {self.first_name}'
            f'{(" " + self.middle_name) if self.middle_name else ""}'
        )

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name', 'first_name', 'middle_name', 'id']
        indexes = [
            models.Index(fields=['is_active', 'position']),
            models.Index(fields=['last_name', 'first_name']),
        ]

    def __str__(self):
        return self.get_full_name()
