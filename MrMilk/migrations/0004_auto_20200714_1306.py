# Generated by Django 3.0.5 on 2020-07-14 07:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('MrMilk', '0003_auto_20200709_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 15, 7, 36, 15, 651788, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 14, 7, 36, 15, 651764, tzinfo=utc)),
        ),
    ]