# Generated by Django 3.1 on 2020-09-03 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0023_auto_20200830_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 5, 10, 53, 59, 694664)),
        ),
    ]
