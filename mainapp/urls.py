from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
import mainapp.views as mainapp
from geekshop import settings

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.catalog, name='cat_index'),
    path('category/<int:pk>/', mainapp.catalog, name='category'),
    #path('category/<int:pk>/page/<int:page>/', mainapp.catalog, name='page'),
    path('product/<int:pk>/', mainapp.detail, name='product'),

    # re_path(r'^product/(P<pk>\d+)/price/$', mainapp.get_product_price, name='product_price'),
]
