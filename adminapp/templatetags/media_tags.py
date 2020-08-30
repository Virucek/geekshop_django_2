from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='media_folder_products')
def media_folder_products(path):
    if not path:
        path = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{path}'

def media_folder_users(path):
    if not path:
        path = 'user_avatars/default.png'

    return f'{settings.MEDIA_URL}{path}'

register.filter('media_folder_users', media_folder_users)