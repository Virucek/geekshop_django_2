from django.urls import path, re_path

import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    re_path(r'^$', ordersapp.OrderList.as_view(), name='orders_list'),
    re_path(r'^create/$', ordersapp.OrderCreate.as_view(), name='order_create'),
    re_path(r'^(?P<pk>\d+)/$', ordersapp.OrderRead.as_view(), name='order_read'),
    re_path(r'^edit/(?P<pk>\d+)$', ordersapp.OrderEdit.as_view(), name='order_update'),
    re_path(r'^delete/(?P<pk>\d+)$', ordersapp.OrderDelete.as_view(), name='order_delete'),

    path('complete/forming/<int:pk>', ordersapp.order_forming_complete, name='order_forming_complete'),
    path('update/<int:pk>/status/', ordersapp.order_forming_complete, name='order_forming_complete'),

    path('product/<int:pk>/price/quantity/', ordersapp.get_product_price_quantity, name='product_price_quantity'),
]