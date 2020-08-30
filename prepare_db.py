# -*- coding: windows-1251 -*-
from mainapp.models import *
from geekshop import settings

# ������ ��� ���������� �� ����� ������������ test_data.json �� fixtures.
# ����� ������������� pk � ����� test_data, ������ ������ ���� ������������
settings.configure()
del_category = ProductCategory.objects.filter(name__in=['������', '�����'])
del_merch_type = MerchType.objects.filter(id = 4)
#del_product = Product.objects.filter(category__in=del_category)

#del_product.delete() - �.�. ���������� ��������� ��������, �������� ������� �������� �� ���������
del_merch_type.delete()
del_category.delete()

print(f'All successful')
