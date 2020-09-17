from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self):
#         for item in self:
#             item.product.quantity += item.product
#             item.product.save()
#         super(BasketQuerySet, self).delete()


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)

    # objects = BasketQuerySet.as_manager()

    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @cached_property
    def get_items_cache(self):
        return self.user.basket.select_related

    @property
    def product_price(self):
        return self.product.price * self.quantity

    @property
    def total_price(self):
        # basket_products = Basket.objects.filter(user=self.user)
        basket_products = self.get_items_cache
        return sum(list(map(lambda x: x.product_price, basket_products)))

    @property
    def total_quantity(self):
        # basket_products = Basket.objects.filter(user=self.user)
        basket_products = self.get_items_cache
        return sum(list(map(lambda x: x.quantity, basket_products)))

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(Basket, self).delete()
    #
    # def save(self):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - Basket.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(Basket, self).save()
