# -*- coding: windows-1251 -*-
import random

from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import os
import json

from basketapp.models import Basket
from django.conf import settings
from mainapp.models import ProductCategory, Product


def get_submenu_list():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk, is_active=True)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk, is_active=True)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = ProductCategory.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return ProductCategory.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk, is_active=True, category__is_active=True)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk, is_active=True, category__is_active=True)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = f'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__is_active=True, is_active=True).order_by('price').\
                select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__is_active=True, is_active=True).order_by('price').\
            select_related('category')


def get_products_by_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_by_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).\
                order_by('price').select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).\
            order_by('price').select_related('category')


def get_products_by_category(pk):
    if settings.LOW_CACHE:
        key = f'products_by_category_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True).select_related('category')


def get_products_quantity_gt_zero():
    if settings.LOW_CACHE:
        key = f'products_quntity_gt_zero'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__is_active=True, is_active=True, quantity__gt=0).\
                select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__is_active=True, is_active=True, quantity__gt=0).\
            select_related('category')


def get_same_products(product):
    same_products = get_products_by_category(product.category.pk).exclude(pk=product.pk)[:4]
    return same_products


def get_hot_product():
    products = get_products_quantity_gt_zero()
    if products:
        return random.sample(list(products), 1)[0]
    return None


def main(request):
    content = {
        'title': 'магазин мерча',
    }
    return render(request, 'mainapp/index.html', context=content)


def catalog(request, pk=None):
    items_on_page = 2
    if pk == 0 or pk is None:
        curr_category = {'pk': 0, 'name': 'Все'}
        catalog_list = get_products_ordered_by_price()
        title = 'каталог товаров'
    else:
        curr_category = get_category(pk)
        catalog_list = get_products_by_category_ordered_by_price(pk)
        title = curr_category.name
    # submenu_list = ProductCategory.objects.filter(is_active=True)
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
        'submenu_list': get_submenu_list(),
        'hot_product': get_hot_product(),
        'category': curr_category,
    }
    return render(request, 'mainapp/catalog.html', context=content)


def contacts(request):
    title = 'контакты'
    if settings.LOW_CACHE:
        key = 'contacts'
        json_data = cache.get(key)
        if json_data is None:
            with open(os.path.join(settings.BASE_DIR, "address.json"), "r", encoding="utf8") as file:
                json_data = json.load(file)
            cache.set(key, json_data)
    else:
        with open(os.path.join(settings.BASE_DIR, "address.json"), "r", encoding="utf8") as file:
            json_data = json.load(file)

    content = {
        'title': title,
        'address_data': json_data,
    }
    return render(request, 'mainapp/contacts.html', context=content)


def detail(request, pk):
    product = get_product(pk)
    title = f'продукт: {product.name}'
    # submenu_list = ProductCategory.objects.filter(is_active=True)
    content = {
        'title': title,
        'product': product,
        'submenu_list': get_submenu_list(),
        'same_products': get_same_products(product),
    }
    return render(request, f'mainapp/product_detail.html', context=content)
