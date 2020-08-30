from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = 'Finish your registration'

    body = f'Please, follow link below to finish your registration, {user.username}, on portal MerchMag! \
              \nLink: {settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, body, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        _error = f'error with user activation! {email}'
        error_message = ''
        if user.activation_key == activation_key and not user.is_activation_key_expired() and not user.is_active:
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        elif user.activation_key != activation_key:
            print(f'{_error} - user_activation key != activation key from request!')
            error_message = 'Просим прощения, но ваш ключ активации недействителен'
        elif user.is_activation_key_expired():
            print(f'{_error} - user_activation key is expired already')
            error_message = 'Просим прощения, но ваш ключ активации уже истек'
        else:
            print(f'{_error} - seems, like user already was activated')
            error_message = 'Кажется, ваша учетная запись была активирована ранее! Поздравляем'
        content = {'error_message': error_message}
        return render(request, 'authapp/verification.html', content)
    except Exception as e:
        print(f'caught exception: {e.args}')
        return HttpResponseRedirect(reverse('main'))


def login(request):
    title = 'вход'

    next_url = request.GET.get('next', '')
    print(f'next_url={next_url}')
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                print(f'33333333333 - {request.POST.keys()}')
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form': login_form,
        'next': next_url,
    }

    return render(request, 'authapp/login.html', context=content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_email(user):
                print(f'Email was sent successfully on {user.email}')
            else:
                print(f'Error while sending email on {user.email}')
            return HttpResponseRedirect(reverse('auth:login'))

    else:
        register_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context=content)


def edit(request):
    title = 'редактирование пользователя'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(data=request.POST, instance=request.user, files=request.FILES)
        profile_form = ShopUserProfileEditForm(data=request.POST, instance=request.user.shopuserprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))

    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/edit.html', context=content)