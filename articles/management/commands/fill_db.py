import json
from os import path

from django.core.management.base import BaseCommand
from articles.models import Category, Article, ArticleCategory, Comment
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
            article['author_id'] = User.objects.get(id=article["author_id"])
            Article(**article).save()

        cat_links = load_from_json('category_links')
        ArticleCategory.objects.all().delete()
        for cat_link in cat_links:
            cat_link['article_guid'] = Article.objects.get(guid=cat_link['article_guid'])
            cat_link['category_guid'] = Category.objects.get(guid=cat_link['category_guid'])
            ArticleCategory(**cat_link).save()

        comments = load_from_json('comments')
        Comment.objects.all().delete()
        for comment in comments:
            comment['article_uid'] = Article.objects.get(guid=comment['article_uid'])
            comment['user_id'] = User.objects.get(id=comment['user_id'])
            Comment(**comment).save()
