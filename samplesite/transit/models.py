from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


class Request(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название перевозки')
    direction = models.CharField(max_length=100, verbose_name='Направление')
    type = models.CharField(max_length=100, verbose_name='Тип груза')
    time = models.DateField(verbose_name='Дата доставки')
    weight = models.FloatField(verbose_name='Масса груза ')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)

    ton = 'Тн'
    kilogram = 'Кг'
    measure_type = [
        (ton, 'Тн'),
        (kilogram, 'Кг')

    ]
    measure_name = models.CharField(max_length=20, choices=measure_type, default=kilogram,
                                    verbose_name="Единица измерения")

    class Meta:
        verbose_name_plural = 'Заявки'
        verbose_name = 'Заявки'
