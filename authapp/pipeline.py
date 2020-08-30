from datetime import datetime, date
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone

from authapp.models import ShopUser
from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':

        api_url = urlunparse(('https',
                             'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(dict(fields=','.join(('bdate', 'sex', 'about', 'screen_name')),
                                        access_token=response['access_token'],
                                        v='5.122')),
                                        None
                             ))

        _response = requests.get(api_url)
        if _response.status_code != 200:
            return
        print(f'API_URL --------- {api_url}')
        print(_response.json())
        data = _response.json()['response'][0]
        if data['sex']:
            if data['sex'] == 1:
                user.gender = ShopUser.FEMALE
            elif data['sex'] == 2:
                user.gender = ShopUser.MALE

        if data['about']:
            user.shopuserprofile.about_me = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            today = timezone.now().date()

            if (bdate.year + 18, bdate.month, bdate.day) > (today.year, today.month, today.day):
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

            user.age = (today - bdate).days / 365

        user.shopuserprofile.social_url = f'http://vk.com/{data["screen_name"]}' if data['screen_name'] else f'http://vk.com/id{data["id"]}'

    elif backend.name == 'google-oauth2':

        print(f'GOOOOOOOOOOGLE RESPONSE {response}')
        api_url = urlunparse(('https', 'people.googleapis.com', f'v1/people/{response["sub"]}', None,
                             urlencode(dict(personFields=','.join(('genders', 'birthdays', 'locales')),
                                            access_token=response['access_token'])),
                             None
                              ))

        _response = requests.get(api_url)
        print(f"GOOOGLE API {api_url}")
        print(f"GOOOGLE RESPONSE {_response.content}")
        if _response.status_code != 200:
            return
        data = _response.json()

        if data['genders']:
            if data['genders'][0]['value'] == 'female':
                user.gender = ShopUser.FEMALE
            elif data['genders'][0]['value'] == 'male':
                user.gender = ShopUser.MALE

        if data['birthdays']:
            day = data['birthdays'][0]['date']['day']
            month = data['birthdays'][0]['date']['month']
            year = data['birthdays'][0]['date']['year']
            today = timezone.now().date()

            if (year + 18, month, day) > (today.year, today.month, today.day):
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
            bdate = date(year, month, day)
            user.age = (today - bdate).days / 365

        if data['locales']:
            user.shopuserprofile.language = data['locales'][0]['value']

        user.shopuserprofile.social_url = user.email

    else:
        return

    user.save()
