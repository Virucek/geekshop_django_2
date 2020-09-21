from django.test import TestCase

from authapp.models import ShopUser
from basketapp.models import Basket
from mainapp.models import ProductCategory, Product


class BasketAppTestCase(TestCase):

    def setUp(self):
        self.category = ProductCategory.objects.create(name='Маски')
        self.product_1 = Product.objects.create(name='Маска1',
                                           category=self.category,
                                           price=2500.00,
                                           quantity=50)
        self.product_2 = Product.objects.create(name='Маска2',
                                           category=self.category,
                                           price=4500.00,
                                           quantity=60)
        self.user_1 = ShopUser.objects.create_user(username='django_test',
                                                 password='geekbrains',
                                                 email='test@test.ru')
        self.user_2 = ShopUser.objects.create_user(username='django_test2',
                                                   password='geekbrains',
                                                   email='test2@test.ru')
        self.basket_1_1 = Basket.objects.create(user=self.user_1,
                                              product=self.product_1,
                                              quantity=14)
        self.basket_1_2 = Basket.objects.create(user=self.user_1,
                                               product=self.product_2,
                                               quantity=10)
        self.basket_2_1 = Basket.objects.create(user=self.user_2,
                                               product=self.product_1,
                                               quantity=18)

    def test_get_item(self):
        _basket = self.basket_1_1.get_item(self.basket_2_1.pk)
        self.assertEqual(_basket, self.basket_2_1)

    def test_get_items_cache(self):
        _basket = self.basket_1_2.get_items_cache
        self.assertEqual(list(_basket), [self.basket_1_1, self.basket_1_2])

    def test_get_product_price(self):
        _basket_price_1 = self.basket_1_1.product_price
        _basket_price_2 = self.basket_2_1.product_price
        self.assertEqual(_basket_price_1, 35000.00)
        self.assertEqual(_basket_price_2, 45000.00)

    def test_get_total_price(self):
        _basket_price_1 = self.basket_1_2.total_price
        _basket_price_2 = self.basket_2_1.total_price
        self.assertEqual(_basket_price_1, 80000.00)
        self.assertEqual(_basket_price_2, 45000.00)

    def test_get_total_quantity(self):
        _basket_price_1 = self.basket_1_1.total_quantity
        _basket_price_2 = self.basket_2_1.total_quantity
        self.assertEqual(_basket_price_1, 24)
        self.assertEqual(_basket_price_2, 18)