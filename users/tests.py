# Create your tests here.

from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from team_work import settings
from .models import User


class TestUsersSmoke(TestCase):
    username = 'araym'
    password = 'lalagaga'
    email = 'ara@ya.ru'

    new_user = {
        'username': 'test_user',
        'first_name': 'Jonatan',
        'last_name': 'Jostar',
        'password1': '$t@rPlatinum',
        'password2': '$t@rPlatinum',
        'email': 'jojo@mail.jp',
        'age': 35,
    }

    update_user = {
        'first_name': 'Joli',
        'age': 20,
    }

    def setUp(self):
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)

    def test_login(self):
        # тестирование авторизации
        response = self.client.get('/')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/users/authorization/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_register(self):
        # тестирование регистрации
        response = self.client.post('/users/registration/', data=self.new_user)
        print(f'test_register - post: {response.status_code}')
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username=self.new_user['username'])
        activation_url = f"{settings.DOMAIN_NAME}/users/verify/{self.new_user['email']}/{user.activation_key}/"
        response = self.client.get(activation_url)
        print(f'test_register - activation_url: {response.status_code}')
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.client.logout()

    def test_user_profile_anonymous(self):
        # тестирование личного кабинета
        response = self.client.get('/users/profile/')
        print(f'test_user_profile_anonymous: {response.status_code}')
        self.assertEqual(response.status_code, 302)  # redirect to authorization

    def test_user_profile_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/users/profile/')
        print(f'test_user_profile_logged_in: {response.status_code}')
        self.assertEqual(response.status_code, 200)  # getting profile edit page


    def tearDown(self):
        pass


class TestPublicProfileSmoke(TestCase):
    def setUp(self):
        # сохранить БД коммандой:
        # python manage.py dumpdata -e=contenttypes -e=auth -o test_db.json
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_public_profile(self):
        # проверка работы публичного профиля пользователя
        for user in User.objects.all():
            response = self.client.get(f'/users/public_profile/{user.pk}/')
            print(f'testing public profile: {response.status_code}')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'users')
