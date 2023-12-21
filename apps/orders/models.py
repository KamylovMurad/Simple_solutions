from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.items.models import Item


class Discount(models.Model):
    name = models.CharField(max_length=55, verbose_name='Название')
    amount = models.PositiveIntegerField(validators=[validators.MaxValueValidator(99)], verbose_name='Процент скидки')

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return f'{self.name}'


class Tax(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    rate = models.PositiveIntegerField(validators=[validators.MaxValueValidator(99)], verbose_name='Ставка налога')

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name='Товары')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость', blank=True, null=True)
    payment_status = models.BooleanField(default=False, verbose_name='Статус оплаты')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Скидка')
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Налог')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id}'

#
# @receiver(post_save, sender=Order)
# def calculate_total_price(sender, instance, created, **kwargs):
#     total_price = sum(item for item in instance.items.all())
#     if instance.discount:
#         total_price -= instance.discount.amount
#     if instance.tax:
#         total_price *= (1 + instance.tax.rate / 100)
#
#     instance.total_price = total_price
#     instance.save()