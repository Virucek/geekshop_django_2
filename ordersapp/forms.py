from django import forms

from mainapp.models import Product
from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='Цена', required=False)
    quantity_rest = forms.CharField(label='Кол-во на складе', required=False)


    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['product'].queryset = Product.get_items().select_related()
    # def clean_quantity(self):
    #     data = self.cleaned_data['quantity']
    #     if data > (self.instance.product.quantity + self.instance.quantity):
    #         raise forms.ValidationError('Товаров на складе не осталось')
    #
    #     return data
