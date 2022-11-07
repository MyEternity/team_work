from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from articles.models import Article, Category, Comment, ArticleLike, CommentLike, Notification


class CategoryTests(TestCase):
    """ Тесты модели Category """

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name='test_category',
            image='category_images/test.png',
        )

        cls.name_field = cls.category._meta.get_field('name')

    def test_verbose_name(self):
        pass