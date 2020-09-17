from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL_BY_CUSTOMER = 'CNL'  # отменен пользователем
    REFUSED = 'RFD'  # отказ в процессе обработки (по тех.причинам, например)

    ORDER_STATUS_CHOISES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PROCEED, 'обрабатывается'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (CANCEL_BY_CUSTOMER, 'отменен пользователем'),
        (REFUSED, 'отказан')
    )

    status = models.CharField(verbose_name='статус', max_length=3,
                              choices=ORDER_STATUS_CHOISES, default=FORMING)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id}'

    @cached_property
    def get_items_cached(self):
        return self.orderitems.select_related()

    @property
    def total_quantity(self):
        # items = self.orderitems.select_related()
        items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, items)))

    def total_price(self):
        # items = self.orderitems.select_related()
        items = self.get_items_cached
        return sum(list(map(lambda x: x.product_price, items)))

    total_price = property(total_price)

    def delete(self):
        for item in self.get_items_cached:
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.status = self.CANCEL_BY_CUSTOMER
        self.save()


# class OrderItemQuerySet(models.QuerySet):
#
#     def delete(self):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super(OrderItemQuerySet, self).delete()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    # objects = OrderItemQuerySet.as_manager()

    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()

    @property
    def product_price(self):
        return self.product.price * self.quantity

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(OrderItem, self).delete()
    #
    # def save(self):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - OrderItem.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(OrderItem, self).save()