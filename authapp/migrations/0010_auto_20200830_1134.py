# Generated by Django 3.1 on 2020-08-30 08:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0009_auto_20200826_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 1, 11, 34, 32, 336423)),
        ),
    ]
