from django.db import models

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class Discount(models.Model):
    start_at = models.DateTimeField(verbose_name='начало', auto_now_add=True)
    end_at = models.DateTimeField(verbose_name='окончание', auto_now=True)
    descx = models.CharField(verbose_name='описание', max_length=255, default='скидка')

    MULTI_PROMO = 'MP'
    USER_PROMO = 'UP'
    ONETIME_PROMO = 'OTP'
    COUPON_PROMO = 'CP'

    DISCOUNT_TYPES = (
        (MULTI_PROMO, 'многоразовая скидка'),
        (USER_PROMO, 'пользовательская скидка'),
        (ONETIME_PROMO, 'одноразовая скидка'),
        (COUPON_PROMO, 'купон')
    )

    discount_type = models.CharField(verbose_name='тип скидки', max_length=99,
                                     choices=DISCOUNT_TYPES, default=MULTI_PROMO)

    discount_value = models.PositiveSmallIntegerField(verbose_name='скидка', default=0)

    numbers = models.PositiveIntegerField(verbose_name='количество применений', blank=True,
                                          null=True)


class DiscountRelate(models.Model):
    discount = models.ForeignKey(Discount, related_name='discountitems', on_delete=models.CASCADE)
    user = models.ForeignKey(ShopUser, related_name='discountusers', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, related_name='discountcategories', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='discountproducts', on_delete=models.CASCADE)
    numbers = models.PositiveIntegerField(verbose_name='оставшееся количество', null=True, blank=True)

    class Meta:
        unique_together = ('discount', 'user', 'category', 'product', )
