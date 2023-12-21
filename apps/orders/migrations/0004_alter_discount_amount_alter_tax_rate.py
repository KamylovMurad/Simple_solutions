# Generated by Django 5.0 on 2023-12-21 13:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_discount_amount_alter_tax_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99)], verbose_name='Процент скидки'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='rate',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99)], verbose_name='Ставка налога'),
        ),
    ]
