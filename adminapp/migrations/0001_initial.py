# Generated by Django 3.1 on 2020-09-20 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0007_auto_20200920_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField(auto_now_add=True, verbose_name='начало')),
                ('end_at', models.DateTimeField(auto_now=True, verbose_name='окончание')),
                ('discount_type', models.CharField(choices=[('MP', 'многоразовая скидка'), ('UP', 'пользовательская скидка'), ('OTP', 'одноразовая скидка'), ('CP', 'купон')], default='MP', max_length=99, verbose_name='тип скидки')),
                ('discount_value', models.PositiveSmallIntegerField(default=0, verbose_name='скидка')),
                ('numbers', models.PositiveIntegerField(blank=True, null=True, verbose_name='количество применений')),
            ],
        ),
        migrations.CreateModel(
            name='DiscountRelate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', models.PositiveIntegerField(blank=True, null=True, verbose_name='оставшееся количество')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discountcategories', to='mainapp.productcategory')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discountitems', to='adminapp.discount')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discountproducts', to='mainapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discountusers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('discount', 'user', 'category', 'product')},
            },
        ),
    ]
