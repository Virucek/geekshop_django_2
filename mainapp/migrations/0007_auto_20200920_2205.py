# Generated by Django 3.1 on 2020-09-20 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20200821_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchtype',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Активный'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Активный'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Активная'),
        ),
    ]