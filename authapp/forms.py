import hashlib
import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from authapp.models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Имя пользователя'
            elif field_name == 'password':
                field.widget.attrs['placeholder'] = 'Пароль'


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'avatar', 'age', 'email', 'gender', 'country')
        widgets = {
            'gender': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'gender':
                field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
            data = self.cleaned_data['age']
            if data < 18:
                raise forms.ValidationError('Вы слишком молоды')

            return data

    def clean_email(self):
        data = self.cleaned_data['email']
        email_domain = data.split('@')
        allowed_mails = [
            'yandex',
            'gmail',
            'test',
         ]
        if email_domain[1].split('.')[0] not in allowed_mails:
            raise forms.ValidationError(f'С данным почтовым сервисом мы не работаем. Только с {allowed_mails}')
        # Проверка почты на уникальность
        try:
            email_db = ShopUser.objects.get(email=data)
        except ShopUser.DoesNotExist:
            email_db = None
        # При редактировании проблема - если не менять почту, то выдается ошибка, что такая почта уже используется.
        # Поэтому, проверяю, менялась ли почта (есть ли она в changed_data) И есть ли она в БД
        try:
            email_changed_data = self.changed_data.index('email')
        except ValueError:
            email_changed_data = None
        if email_db and email_changed_data != None:
            raise forms.ValidationError(f'Аккаунт с данным почтовым ящиком уже зарегистрирован')

        return data


class ShopUserRegisterForm(UserCreationForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'gender', 'avatar', 'age', 'email', 'country', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        GENDER_CHOICES = [
            (True, 'male'),
            (False, 'female')
        ]
        for field_name, field in self.fields.items():
            if field_name == 'gender':
                field.widget = forms.RadioSelect(choices=GENDER_CHOICES)
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды')

        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        email_domain = data.split('@')
        allowed_mails = [
            'yandex',
            'gmail',
            'test',
        ]
        if email_domain[1].split('.')[0] not in allowed_mails:
            raise forms.ValidationError(f'С данным почтовым сервисом мы не работаем. Только с {allowed_mails}')
        # Проверка почты на уникальность
        try:
            email_db = ShopUser.objects.get(email=data)
        except ShopUser.DoesNotExist:
            email_db = None

        if email_db:
            raise forms.ValidationError(f'Аккаунт с данным почтовым ящиком уже зарегистрирован')

        return data

    def save(self):
        user = super(ShopUserRegisterForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1(str(user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserProfileEditForm(forms.ModelForm):

    class Meta:
        model = ShopUserProfile
        fields = ('tagline', 'about_me', 'social_url')

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

