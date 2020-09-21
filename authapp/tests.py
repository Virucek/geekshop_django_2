from django.core.management import call_command
from django.test import TestCase, Client

from authapp.models import ShopUser


GOOD_STATUS_CODE = 200
REDIRECT_STATUS_CODE = 302


class AuthAppTestCase(TestCase):

    def setUp(self):
        call_command('loaddata', 'test_db_9_21_20201.json')
        self.client = Client()

        self.supername = 'test_superdjango'
        self.superpassword = 'geekbrains'
        self.superuser = ShopUser.objects.create_superuser(username=self.supername,
                                                           email='test@test.ru',
                                                           password=self.superpassword)

        self._username = 'test_django'
        self._password = 'geekbrains'
        self._first_name = 'Name_Django'
        self._user = ShopUser.objects.create_user(username=self._username,
                                                 email='test1@test.ru',
                                                 password=self._password,
                                                 first_name=self._first_name)

        self.new_username = 'test_new_django'
        self.new_password = 'megageekbrains'
        self.new_first_name = 'Name_Test'
        self.new_email = 'new_email@test.ru'

    # Логин суперпользователя
    def test_superuser_login(self):
        # зайти на сайт незалогиненным
        response = self.client.get('/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        # to do: Поправить вывод имени при его отсутствии. Сменить 'пользователь' на 'аноним', если юзер не авторизовался
        # self.assertNotContains(response.content, 'Пользователь')
        self.assertTrue(response.context['user'].is_anonymous)

        # Перейти на страницу логина
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.assertTrue(response.context['user'].is_anonymous)

        # Залогиниться
        self.client.login(username=self.supername, password=self.superpassword)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)

        # Проверка главной
        response = self.client.get('/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.assertContains(response, 'Пользователь')
        self.assertContains(response, 'Админка')
        self.assertContains(response, 'Выход')

    # Логин простого пользователя
    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.assertTrue(response.context['user'].is_anonymous)

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.client.login(username=self._username, password=self._password)

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self._user)

        response = self.client.get('/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.assertNotContains(response, 'Админка')
        self.assertNotContains(response, 'Пользователь')
        self.assertContains(response, self._first_name)
        self.assertContains(response, 'Выход')

#     Регистрация
    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.assertTrue(response.context['user'].is_anonymous)

        user_data = {
            'username': self.new_username,
            'first_name': self.new_first_name,
            'gender': True,
            'age': 35,
            'email': self.new_email,
            'password1': self.new_password,
            'password2': self.new_password
        }

        response = self.client.post('/auth/register/', data=user_data)
        self.assertEqual(response.status_code, REDIRECT_STATUS_CODE)

        new_user = ShopUser.objects.filter(username=self.new_username).first()
        self.assertEqual(new_user.first_name, user_data['first_name'], msg='First user name is not OK.')
        self.assertEqual(new_user.age, user_data['age'], msg='Age is NOT OK.')
        self.assertEqual(new_user.email, user_data['email'], msg='Email is NOT OK.')
        self.assertEqual(new_user.is_active, 0, msg='User is active, it\'s NOT OK.')

        # Попытаться залогиниться под ещё не активированным пользователем
        self.client.login(username=self.new_username, password=self.new_password)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.assertTrue(response.context['user'].is_anonymous)

        # Верификация пользователя
        verify_link = f'/auth/verify/{user_data["email"]}/{new_user.activation_key}/'
        response = self.client.get(verify_link)
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        # to do: Добавить title
        # self.assertEqual(response.context['title'], 'Аутентификация')
        self.assertContains(response, 'Поздравляем, ты окончил свою регистрацию!')

        # Логин под верифицированным пользователем
        self.client.login(username=self.new_username, password=self.new_password)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.assertFalse(response.context['user'].is_anonymous)
        new_user = ShopUser.objects.filter(username=self.new_username).first()
        self.assertEqual(new_user.is_active, 1)

        # Проверка главной
        response = self.client.get('/')
        self.assertEqual(response.status_code, GOOD_STATUS_CODE)
        self.assertContains(response, user_data['first_name'])
        self.assertNotContains(response, 'Админка')
        self.assertContains(response, 'Выход')
