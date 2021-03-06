import requests
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem

URL_CHECK_FAILED = 'orders:orders_list'


def required_status(statuses):
    def decorator(function):
        def wrapper(_self, *args, **kwargs):
            # print(kwargs)
            # print(f'request {request.__dict__}')
            # if kwargs:
            #     _object = Order.objects.filter(pk=kwargs['pk']).first()
            _object = _self.get_object()
            if _object:
                if _object.status in statuses:
                    return function(_self, *args, **kwargs)
                else:
                    return HttpResponseRedirect(reverse(URL_CHECK_FAILED))
        return wrapper
    return decorator


def correct_user(function):
    def wrapper(_self, *args, **kwargs):
        if _self.request.user:
            # _object = Order.objects.filter(pk=kwargs['pk']).first()
            _object = _self.get_object()
            if _object:
                if _object.user == _self.request.user:
                    return function(_self, *args, **kwargs)
                else:
                    return HttpResponseRedirect(reverse(URL_CHECK_FAILED))
    return wrapper


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
        # return Order.objects.filter(user=self.request.user)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                    form.initial['quantity_rest'] = basket_items[num].product.quantity
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        Basket.objects.filter(user=self.request.user).delete()
        orderitems = context['orderitems']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        return super(OrderCreate, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OrderRead(DetailView):
    model = Order

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OrderEdit(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    # @method_decorator(correct_user)
    @method_decorator(login_required())
    @correct_user
    @required_status(statuses=(Order.FORMING,))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(OrderEdit, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
                    form.initial['quantity_rest'] = form.instance.product.quantity

        data['orderitems'] = formset
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        
        return super(OrderEdit, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:orders_list')

    # @method_decorator(correct_user)
    # @method_decorator(required_status(statuses=(Order.FORMING,)))
    @method_decorator(login_required())
    @correct_user
    @required_status((Order.FORMING,))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orders:orders_list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    # print(f'update_fields -- {update_fields}')
    # if update_fields is 'products' or 'quantity':
    if instance.pk:
        if sender.get_item(instance.pk) is not None: # для миграции БД
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        # instance.product.quantity = F('quantity') - sender.get_item(instance.pk).quantity
    else:
        # instance.product.quantity = F('quantity') - instance.quantity
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    # instance.product.quantity = F('quantity') + instance.quantity
    instance.product.save()


def get_product_price_quantity(request, pk):
    if request.is_ajax():
        product = Product.objects.get(pk=int(pk))
        return JsonResponse({'price': product.price, 'quantity': product.quantity})
