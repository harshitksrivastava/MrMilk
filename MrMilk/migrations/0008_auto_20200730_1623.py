# Generated by Django 3.0.5 on 2020-07-30 10:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('MrMilk', '0007_auto_20200729_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 31, 10, 53, 30, 213009, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 30, 10, 53, 30, 212984, tzinfo=utc)),
        ),
    ]