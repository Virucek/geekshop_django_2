# -*- coding: windows-1251 -*-
from mainapp.models import *
from geekshop import settings

# Скрипт для подготовки БД перед перезаливкой test_data.json из fixtures.
# Когда предопределил pk в файле test_data, данный скрипт стал неактуальным
settings.configure()
del_category = ProductCategory.objects.filter(name__in=['Брелок', 'Шапка'])
del_merch_type = MerchType.objects.filter(id = 4)
#del_product = Product.objects.filter(category__in=del_category)

#del_product.delete() - т.к. используем каскадное удаление, отдельно удалять продукты не требуется
del_merch_type.delete()
del_category.delete()

print(f'All successful')
