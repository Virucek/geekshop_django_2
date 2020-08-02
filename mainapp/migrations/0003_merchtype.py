# Generated by Django 3.0.8 on 2020-08-02 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Имя типа мерча')),
                ('descx', models.TextField(blank=True, verbose_name='Описание типа')),
            ],
        ),
    ]
