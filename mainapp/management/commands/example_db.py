from django.core.management import BaseCommand
from django.db import connection
from django.db.models import Q

from adminapp.views import db_profile_by_type
from mainapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_products = Product.objects.filter(
            Q(category__name='Постеры') |
            Q(category__name='Кружки')
        ).select_related()

        print(len(test_products))

        db_profile_by_type('learn_db', '', connection.queries)
        print(test_products)