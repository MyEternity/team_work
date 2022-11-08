from django.test import TestCase

from articles.models import Article, Category, Comment, ArticleLike, CommentLike, Notification


class CategoryTests(TestCase):
    """ Тесты модели Category """

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            guid='b2695f9c-ad29-4e9b-a63e-55e788d6dd13',
            image='category_images/test.png',
        )

        cls.guid_field = cls.category._meta.get_field('guid')
        cls.name_field = cls.category._meta.get_field('name')
        cls.image_field = cls.category._meta.get_field('image')
        cls.is_active_field = cls.category._meta.get_field('is_active')

    def test_guid_verbose_name(self):
        real_gid_verbose_name = getattr(self.guid_field, 'verbose_name')
        expected_guid_verbose_name = 'Ключ'
        self.assertEqual(real_gid_verbose_name, expected_guid_verbose_name)

    def test_guid_max_length(self):
        real_guid_max_length = getattr(self.guid_field, 'max_length')
        expected_guid_max_length = 64
        self.assertEqual(real_guid_max_length, expected_guid_max_length)

    def test_name_verbose_name(self):
        real_name_verbose_name = getattr(self.name_field, 'verbose_name')
        expected_name_verbose_name = 'Наименование'
        self.assertEqual(real_name_verbose_name, expected_name_verbose_name)

    def test_name_max_length(self):
        real_name_verbose_name = getattr(self.name_field, 'max_length')
        expected_name_max_length = 128
        self.assertEqual(real_name_verbose_name, expected_name_max_length)

    def test_image_verbose_name(self):
        real_image_verbose_name = getattr(self.image_field, 'verbose_name')
        expected_image_verbose_name = 'Изображение'
        self.assertEqual(real_image_verbose_name, expected_image_verbose_name)

    def test_image_max_length(self):
        real_image_max_length = getattr(self.image_field, 'max_length')
        expected_image_max_length = 255
        self.assertEqual(real_image_max_length, expected_image_max_length)

    def test_is_active_verbose_name(self):
        real_is_active_verbose_name = getattr(self.is_active_field, 'verbose_name')
        expected_is_active_verbose_name = 'Активность'
        self.assertEqual(real_is_active_verbose_name, expected_is_active_verbose_name)

    def test_is_active_default(self):
        real_is_active_default = getattr(self.is_active_field, 'default')
        self.assertTrue(real_is_active_default)

    def test_model_choices(self):
        real_model_choices = self.category.choices()
        expected_model_choices = [('b2695f9c-ad29-4e9b-a63e-55e788d6dd13', 'Нет категории')]
        self.assertEqual(real_model_choices, expected_model_choices)

    def test_model_verbose_name(self):
        self.assertEqual(self.category._meta.verbose_name, 'Категория')

    def test_model_verbose_name_plural(self):
        self.assertEqual(self.category._meta.verbose_name_plural, 'Категории')

    def test_string_representation(self):
        self.assertEqual(str(self.category), str(self.category.name))
