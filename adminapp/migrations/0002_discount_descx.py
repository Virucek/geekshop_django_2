# Generated by Django 3.1 on 2020-09-20 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='descx',
            field=models.CharField(default='скидка', max_length=255, verbose_name='описание'),
        ),
    ]