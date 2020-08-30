from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=100, unique=True)
    descx = models.TextField(verbose_name='Описание категории', blank=True)
    is_active = models.BooleanField(verbose_name='Активная', default=True)

    def __str__(self):
        return self.name


class MerchType(models.Model):
    name = models.CharField(verbose_name='Имя типа мерча', max_length=100, unique=True)
    descx = models.TextField(verbose_name='Описание типа', blank=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, verbose_name='Название категории', on_delete=models.CASCADE)
    merch_type = models.ForeignKey(MerchType, verbose_name='Тип мерча', on_delete=models.CASCADE, blank=True, default=None, null=True)
    name = models.CharField(verbose_name='Название продукта', max_length=100)
    image = models.ImageField(verbose_name='Изображение', upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='Краткое описание продукта', max_length=100, blank=True)
    full_desc = models.TextField(verbose_name='Полное описание продукта', blank=True)
    price = models.DecimalField(verbose_name='Цена продукта', max_digits=6, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество продукта на складе', default=0)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    def __str__(self):
        return f'{self.name} -- {self.category.name}'
