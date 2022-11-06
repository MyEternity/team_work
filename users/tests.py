# Create your tests here.
import unittest
from unittest.mock import patch
from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from .views import AuthorizationView, RegistrationView, UserProfileView, UserLogoutView, PublicUserProfileView
from .models import User, UserProfile


class TestUsersSmoke(TestCase):
    username = 'oraora'
    email = 'mudamuda@muda.ru'
    password = 'yareyare'

    new_user = {
        'username': 'test_user',
        'first_name': 'Jonatan',
        'last_name': 'Jostar',
        'password1': '$t@rPlatinum',
        'password2': '$t@rPlatinum',
        'email': 'jojo@mail.jp',
        'age': 35,
    }

    def setUp(self):
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/users/authorization/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass

    # app_name = 'users'
    # path('authorization/', AuthorizationView.as_view(), name='authorization'),
    # path('logout', UserLogoutView.as_view(), name='logout'),
    # path('registration/', RegistrationView.as_view(), name='registration'),
    # path('profile/', UserProfileView.as_view(), name='profile'),
    # path('public_profile/<int:pk>/', PublicUserProfileView.as_view(), name='public_profile'),
    # path('verify/<str:email>/<str:activate_key>/', RegistrationView.verify, name='verify'),
