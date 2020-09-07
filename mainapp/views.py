# -*- coding: windows-1251 -*-
import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import os
import json

from basketapp.models import Basket
from geekshop import settings
from mainapp.models import ProductCategory, Product


def get_same_products(product):
    same_products = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    return same_products


def get_hot_product():
    products = Product.objects.filter(category__is_active=True, is_active=True, quantity__gt=0)
    return random.sample(list(products), 1)[0]


def main(request):
    content = {
        'title': 'магазин мерча',
    }
    return render(request, 'mainapp/index.html', context=content)


def catalog(request, pk=None):
    items_on_page = 2
    if pk == 0 or pk is None:
        curr_category = {'pk': 0, 'name': 'Все'}
        catalog_list = Product.objects.filter(category__is_active=True, is_active=True).order_by('price')
        title = 'каталог товаров'
    else:
        curr_category = get_object_or_404(ProductCategory, pk=pk, is_active=True)
        catalog_list = Product.objects.filter(category=pk, is_active=True).order_by('price')
        title = curr_category.name
    submenu_list = ProductCategory.objects.filter(is_active=True)
    page = request.GET.get('page')
    paginator = Paginator(catalog_list, items_on_page)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {
        'title': title,
        'catalog_list': products_paginator,
        'submenu_list': submenu_list,
        'hot_product': get_hot_product(),
        'category': curr_category,
    }
    return render(request, 'mainapp/catalog.html', context=content)


def contacts(request):
    with open(os.path.join(settings.BASE_DIR, "address.json"), "r", encoding="utf8") as file:
        json_data = json.load(file)

    content = {
        'title': 'контакты',
        'address_data': json_data,
    }
    return render(request, 'mainapp/contacts.html', context=content)


def detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True, category__is_active=True)
    title = f'продукт: {product.name}'
    submenu_list = ProductCategory.objects.filter(is_active=True)
    content = {
        'title': title,
        'product': product,
        'submenu_list': submenu_list,
        'same_products': get_same_products(product),
    }
    return render(request, f'mainapp/product_detail.html', context=content)
