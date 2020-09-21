from django.test import TestCase

from mainapp.models import ProductCategory, Product


class MainAppCatalogTestCase(TestCase):

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

    def test_print(self):
        _product_1 = Product.objects.get(name='Маска1')
        _product_2 = Product.objects.get(name='Маска2')
        self.assertEqual(str(_product_1), 'Маска1 -- Маски')
        self.assertEqual(str(_product_2), 'Маска2 -- Маски')

    def test_get_items(self):
        _product_1 = Product.objects.get(name='Маска1')
        _product_2 = Product.objects.get(name='Маска2')
        _products = self.product_1.get_items()
        self.assertEqual(list(_products), [_product_1, _product_2])