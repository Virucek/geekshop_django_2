# Generated by Django 3.1 on 2020-08-30 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0015_auto_20200830_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 1, 19, 10, 56, 28667)),
        ),
    ]