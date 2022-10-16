import json
from os import path

from django.core.management.base import BaseCommand
from articles.models import Category, Article, ArticleCategory
from users.models import User

JSON_PATH = 'articles/json'


def load_from_json(file_name):
    with open(path.join(JSON_PATH, file_name + '.json'), 'r') as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        Category.objects.all().delete()

        for category in categories:
            new_category = Category(**category)
            new_category.save()

        users = load_from_json('users')
        User.objects.all().delete()

        for user in users:
            new_user = User(**user)
            new_user.save()

        articles = load_from_json('articles')
        Article.objects.all().delete()

        for article in articles:
            # category_id = article["category_id"]
            # _category = ArticleCategory.objects.get(guid=category_id)
            # article['category_id'] = _category

            author_id = article["author_id"]
            _author = User.objects.get(id=author_id)
            article['author_id'] = _author

            new_article = Article(**article)
            new_article.save()

        cat_links = load_from_json('category_links')
        ArticleCategory.objects.all().delete()

        for cat_link in cat_links:
            art = Article.objects.get(guid=cat_link['article_guid'])
            cat = Category.objects.get(guid=cat_link['category_guid'])
            cat_link['article_guid'] = art
            cat_link['category_guid'] = cat
            new_cat_link = ArticleCategory(**cat_link)
            new_cat_link.save()
