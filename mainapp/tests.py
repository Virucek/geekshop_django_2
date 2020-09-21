from django.core.management import call_command
from django.test import TestCase, Client

from mainapp.models import ProductCategory, Product

STATUS_CODE_GOOD = 200


class MainAppTestCase(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db_9_21_20201.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, STATUS_CODE_GOOD)
        self.assertEqual(response.context['title'], 'магазин мерча')

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, STATUS_CODE_GOOD)
        self.assertEqual(response.context['title'], 'контакты')

        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, STATUS_CODE_GOOD)
        self.assertEqual(response.context['title'], 'каталог товаров')
        # self.assertNotContains(response, 'Горячее предложение')

        response = self.client.get('/catalog/category/0/')
        self.assertEqual(response.status_code, STATUS_CODE_GOOD)
        self.assertEqual(response.context['title'], 'каталог товаров')

        # categories = ProductCategory.objects.all()
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/catalog/category/{category.pk}/')
            self.assertEqual(response.status_code, STATUS_CODE_GOOD)
            self.assertEqual(response.context['title'], category.name)

        for product in Product.objects.all():
            response = self.client.get(f'/catalog/product/{product.pk}/')
            self.assertEqual(response.status_code, STATUS_CODE_GOOD)
            self.assertEqual(response.context['title'], f'продукт: {product.name}')

    def teardown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')