from django.conf import settings
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)

    @property
    def product_price(self):
        return self.product.price * self.quantity

    @property
    def total_price(self):
        basket_products = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.product_price, basket_products)))

    @property
    def total_quantity(self):
        basket_products = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.quantity, basket_products)))
