from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    title = 'Корзина товаров'
    baskets = Basket.objects.filter(user=request.user).select_related()

    content = {
        'title': title,
        'baskets': baskets,
    }
    return render(request, 'basketapp/basket.html', context=content)


@login_required
def basket_add(request, pk):
    print('11111111111111111')
    print('22222222222222222')
    product = get_object_or_404(Product, pk=pk)
    if product.quantity == 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if basket:
        basket.quantity = F('quantity') + 1
    else:
        basket = Basket(user=request.user, product=product, quantity=1)

    # if not basket:
    #     basket = Basket(user=request.user, product=product)

    # basket.quantity += 1
    # print(F('quantity'))
    basket.save()

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('catalog:product', args=[pk]))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Удаление продукта из корзины
@login_required
def basket_remove(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():

        quantity = int(quantity)
        basket = Basket.objects.get(pk=int(pk))
        errorText = ''

        if basket.product.quantity > 0 or quantity < basket.quantity:
            if quantity > 0:
                basket.quantity = quantity
                basket.save()
            else:
                basket.delete()
        else:
            errorText = 'На складе не осталось данного товара'

        basket_items = Basket.objects.filter(user=request.user)

        content = {
            'baskets': basket_items,
        }

        result_list = render_to_string('basketapp/includes/inc_basket_list.html', context=content)
        result_total = render_to_string('basketapp/includes/inc_basket_footer.html', context=content)
        response_data = {
            'result_list': result_list,
            'result_total': result_total,
        }
        if errorText:
            response_data.update({'errorText': errorText})

        return JsonResponse(response_data)
