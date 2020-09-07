from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryAdminEditForm, ProductAdminEditForm, \
    MerchTypeAdminEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, MerchType
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem

# список финальных статусов заказа, при которых его нельзя изменить или отменить
FINAL_ORDER_STATUSES = (
    Order.READY,
    Order.CANCEL_BY_CUSTOMER,
    Order.REFUSED,
)
# список названий кнопок для перехода по статусам. (для шаблона)
STATUS_ORDER_BUTTONS = (
    (Order.FORMING, 'Отправить в обработку'),
    (Order.SENT_TO_PROCEED, 'Обработать'),
    (Order.PROCEED, 'Оплатить'),
    (Order.PAID, 'Готов'),
)


class ClassBasedViewMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = getattr(self, 'title')
        category_data = getattr(self, 'category', None)

        if category_data is not None:
            context['category'] = category_data

        return context

    def dispatch(self, *args, **kwargs):
        disp = super().dispatch
        decorators = getattr(self, 'decorators', [user_passes_test(lambda u: u.is_superuser)])

        for decorator in decorators:
            disp = decorator(disp)

        return disp(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class UsersListView(ClassBasedViewMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    title = 'админка / пользователи'

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    # def dispatch(self, request, *args, **kwargs):
    #     return user_passes_test(lambda u: u.is_superuser)(super().dispatch)(request, *args, **kwargs)


class UserCreateView(ClassBasedViewMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserRegisterForm
    title = 'пользователи / создание'


class UserEditView(ClassBasedViewMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserAdminEditForm
    title = 'пользователи / редактирование'


class UserDeleteView(ClassBasedViewMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')
    title = 'пользователи / удаление'


class CategoriesListView(ClassBasedViewMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    title = 'админка / категории'


class CategoryCreateView(ClassBasedViewMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'
    title = 'категории / создание'


class CategoryEditView(ClassBasedViewMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'
    title = 'категории / редактирование'


class CategoryDeleteView(ClassBasedViewMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')
    title = 'категории / удаление'


class ProductsListView(ClassBasedViewMixin, ListView):
    paginate_by = 3
    model = Product
    template_name = 'adminapp/products.html'
    title = 'категории / товары'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_pk = self.kwargs['pk']
        context['category'] = ProductCategory.objects.get(pk=category_pk)
        return context


class ProductDetailView(ClassBasedViewMixin, DetailView):
    model = Product
    template_name = 'adminapp/product.html'
    title = 'товар / подробнее'


class ProductCreateView(ClassBasedViewMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'
    title = 'товары / создание'

    def get_success_url(self):
        category_id = self.kwargs['pk']
        return reverse_lazy('admin:products', kwargs={'pk': category_id})

    def get_initial(self):
        category = ProductCategory.objects.get(pk=self.kwargs['pk'])
        return {'category': category}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        context['category'] = ProductCategory.objects.get(pk=category_id)
        return context


class ProductEditView(ClassBasedViewMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'
    title = 'товары / редактирование'

    def get_success_url(self):
        product = Product.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy('admin:products', kwargs={'pk': product.category.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(pk=self.kwargs['pk'])
        context['category'] = product.category
        return context


class ProductDeleteView(ClassBasedViewMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    title = 'товары / удаление'

    def get_success_url(self):
        product = Product.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy('admin:products', kwargs={'pk': product.category.id})


class MerchTypesListView(ClassBasedViewMixin, ListView):
    model = MerchType
    template_name = 'adminapp/merch_types.html'
    title = 'админка / типы мерча'


class MerchTypeCreateView(ClassBasedViewMixin, CreateView):
    model = MerchType
    template_name = 'adminapp/merch_type_update.html'
    success_url = reverse_lazy('admin:merch_types')
    fields = '__all__'
    title = 'типы мерча / создание'


class MerchTypeEditView(ClassBasedViewMixin, UpdateView):
    model = MerchType
    template_name = 'adminapp/merch_type_update.html'
    success_url = reverse_lazy('admin:merch_types')
    fields = '__all__'
    title = 'типы мерча / редактирование'


class MerchTypeDeleteView(ClassBasedViewMixin, DeleteView):
    model = MerchType
    template_name = 'adminapp/merch_type_delete.html'
    success_url = reverse_lazy('admin:merch_types')
    title = 'типы мерча / удаление'


class OrdersListView(ClassBasedViewMixin, ListView):
    model = Order
    title = 'админка / заказы'
    template_name = 'adminapp/orders.html'
    extra_context = {'DISABLED_ORDER_STATUSES': DISABLED_ORDER_STATUSES, 'STATUS_ORDER_BUTTONS': STATUS_ORDER_BUTTONS}


class OrderCreateView(ClassBasedViewMixin, CreateView):
    model = Order
    title = 'заказы / создание'
    fields = ['user', 'status']
    template_name = 'adminapp/order_update.html'
    success_url = reverse_lazy('admin:orders')

    def get_context_data(self, **kwargs):
        data = super(OrderCreateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            formset = OrderFormSet()

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

        return super(OrderCreateView, self).form_valid(form)


class OrderDetailView(ClassBasedViewMixin, DetailView):
    model = Order
    template_name = 'adminapp/order.html'
    title = 'заказы / подробнее'
    extra_context = {'DISABLED_ORDER_STATUSES': DISABLED_ORDER_STATUSES, 'STATUS_ORDER_BUTTONS': STATUS_ORDER_BUTTONS}


class OrderUpdateView(ClassBasedViewMixin, UpdateView):
    model = Order
    title = 'заказы / редактирование'
    fields = ['status']
    template_name = 'adminapp/order_update.html'
    success_url = reverse_lazy('admin:orders')

    def get_context_data(self, **kwargs):
        data = super(OrderUpdateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)

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

        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(ClassBasedViewMixin, DeleteView):
    model = Order
    title = 'заказы / удаление'
    template_name = 'adminapp/order_delete.html'
    success_url = reverse_lazy('admin:orders')

# если заказ удаляется, ему присваивается статус "отменен"
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
            self.object.status = Order.REFUSED
        else:
            self.object.is_active = True
            self.object.status = Order.FORMING
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def order_status_next(request, pk):
    object = get_object_or_404(Order, pk=pk)
    statuses = Order.ORDER_STATUS_CHOISES
    if object.status in FINAL_ORDER_STATUSES:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    for i in range(len(statuses)):
        print(object.status, i, len(statuses))
        if object.status == statuses[i][0]:
            object.status = statuses[i + 1][0]
            object.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda u: u.is_superuser)
def order_cancel_customer(request, pk):
    object = get_object_or_404(Order, pk=pk)
    if object.status in FINAL_ORDER_STATUSES:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    object.status = Order.CANCEL_BY_CUSTOMER
    object.is_active = False
    object.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
