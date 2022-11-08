from django.test import TestCase
from django.test import RequestFactory

from .fixtures.articles import article_1, article_2
from bs4 import BeautifulSoup
from users.models import User
from articles.models import Article
from articles.views import IndexListView, preview_handler


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

    def test_is_one_images_stay(self):
        queryset = Article.objects.all()
        preview_handler(queryset, 100)
        real_images_count = 0

        for article in queryset:
            article_body = BeautifulSoup(article.article_body, 'html.parser')
            real_images_count = sum([1 for _ in article_body.select('img')])
            if real_images_count > 1:
                break
        self.assertTrue(real_images_count <= 1)
