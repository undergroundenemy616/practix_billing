# Generated by Django 4.0.2 on 2022-02-27 01:09

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribtions', '0007_alter_tariff_period'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='paid_period',
        ),
        migrations.AlterField(
            model_name='tariff',
            name='period',
            field=models.DurationField(choices=[(datetime.timedelta(days=7), 'Week'), (datetime.timedelta(days=30), 'Month'), (datetime.timedelta(days=356), 'Year')], default=datetime.timedelta(days=30), verbose_name='Период подписки'),
        ),
    ]
