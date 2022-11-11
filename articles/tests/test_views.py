from django.test import TestCase, RequestFactory, Client
from django.utils.html import strip_tags

from .fixtures.articles import article_1, article_2
from bs4 import BeautifulSoup
from users.models import User
from articles.models import Article
from articles.views import preview_handler, IndexListView


class PreviewHandlerTests(TestCase):
    """ Тесты функции preview_handler """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_author',
            email='test@mail.com'
        )

        cls.article1 = Article.objects.create(
            author_id=cls.user,
            topic=article_1.topic,
            article_body=article_1.body
        )

        cls.article2 = Article.objects.create(
            author_id=cls.user,
            topic=article_2.topic,
            article_body=article_2.body
        )

    def test_is_queryset_stay(self):
        queryset = Article.objects.all()
        expected_type = type(queryset)
        preview_handler(queryset, 100)
        real_type = type(queryset)
        self.assertEqual(real_type, expected_type)

    def test_is_one_image_stay(self):
        queryset = Article.objects.all()
        preview_handler(queryset, 100)
        real_images_count = 0

        for article in queryset:
            article_body = BeautifulSoup(article.article_body, 'html.parser')
            real_images_count = sum([1 for _ in article_body.select('img')])
            if real_images_count > 1:
                break
        self.assertLessEqual(real_images_count, 1)

    def test_truncatechars(self):
        expected_chars_count = 100
        queryset = Article.objects.all()
        preview_handler(queryset, expected_chars_count)
        real_chars_count = 0

        for article in queryset:
            real_chars_count = len(strip_tags(article.article_body))
            if real_chars_count != expected_chars_count:
                break
        self.assertEqual(real_chars_count, expected_chars_count)


class IndexListViewTests(TestCase):
    """ Тесты функции preview_handler """

    @classmethod
    def setUpTestData(cls):
        cls.view = IndexListView()
        roles = ['user', 'moder', 'admin']

        for role in roles:
            User.objects.create(username=role,
                                email=f'{role}@mail.com',
                                is_active=True,
                                is_staff=True if role in ('moder', 'admin') else False,
                                is_superuser=True if role == 'admin' else False)

        cls.user = User.objects.get(username='user')
        cls.moder = User.objects.get(username='moder')
        cls.admin = User.objects.get(username='admin')

        cls.article1 = Article.objects.create(
            author_id=cls.user,
            topic=article_1.topic,
            article_body=article_1.body
        )

        cls.article2 = Article.objects.create(
            author_id=cls.user,
            topic=article_2.topic,
            article_body=article_2.body
        )

    def test_is_guest_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_is_user_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_is_moder_200(self):
        self.client.force_login(self.moder)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_is_admin_200(self):
        self.client.force_login(self.admin)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_show_publicated_only(self):
        request = RequestFactory().get('/')
        self.view.request = request
        queryset = self.view.get_queryset()

        real_values = [article.publication for article in queryset]

        self.assertNotIn(False, real_values, msg="В IndexListView присутствуют неопубликованные статьи!")
