from django import forms

from adminapp.models import Discount
from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, MerchType


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryAdminEditForm(forms.ModelForm):
    # discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=100, initial=0)

    class Meta:
        model = ProductCategory
        # fields = '__all__'
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductAdminEditForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MerchTypeAdminEditForm(forms.ModelForm):
    class Meta:
        model = MerchType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DiscountAdminEditForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
