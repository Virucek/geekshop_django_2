import json
import os

from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from geekshop import settings
from mainapp.models import ProductCategory, MerchType, Product

JSON_PATH = os.path.join(settings.BASE_DIR, 'db_json')


def load_data(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding="UTF-8") as file:
        return json.load(file)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        categories = load_data('categories')
        # print(categories)
        ProductCategory.objects.all().delete()
        for cat in categories:
            ProductCategory.objects.create(**cat)

        merch_types = load_data('merch_types')

        MerchType.objects.all().delete()
        for mtype in merch_types:
            MerchType.objects.create(**mtype)

        products = load_data('products')

        for product in products:
            cat_name = product['category']
            _category = ProductCategory.objects.get(name=cat_name)

            product['category'] = _category

            merch_type_name = product['merch_type']
            _mtype = MerchType.objects.get(name=merch_type_name)

            product['merch_type'] = _mtype

            Product.objects.create(**product)

        # Добавление суперпользователя
        # ShopUser.objects.filter(username='django').delete()
        ShopUser.objects.all().delete()
        super_user = ShopUser.objects.create_superuser('django', 'django@gmail.com', 'geekbrains', age=26, first_name='admin')