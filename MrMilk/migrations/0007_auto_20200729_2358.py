# Generated by Django 3.0.5 on 2020-07-29 18:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('MrMilk', '0006_auto_20200729_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 30, 18, 28, 54, 981482, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 29, 18, 28, 54, 981456, tzinfo=utc)),
        ),
    ]
