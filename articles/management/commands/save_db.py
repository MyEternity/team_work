import json
from os import path

from django.core.management.base import BaseCommand
from articles.models import Article, ArticleCategory, Category, Comment
from users.models import User

JSON_PATH = 'articles/json'


def save_json(file_name, data):
    with open(path.join(JSON_PATH, file_name + '.json'), 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=4, sort_keys=True, default=str)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = Category.objects.all()
        data = []
        for category in categories:
            data.append({'guid': category.guid,
                         'name': category.name,
                         'image': str(category.image),
                         'is_active': category.is_active})

        save_json('categories', data)

        users = User.objects.all()
        data = []
        for user in users:
            data.append({'id': user.id,
                         'username': user.username,
                         'password': user.password,
                         'email': user.email,
                         'is_superuser': user.is_superuser,
                         'is_staff': user.is_staff})

            save_json('users', data)

        articles = Article.objects.all()
        data = []
        for article in articles:
            data.append({'guid': article.guid,
                         'author_id': article.author_id.id,
                         'topic': article.topic,
                         'creation_date': article.creation_date,
                         'blocked': article.blocked,
                         'moderation': article.moderation,
                         'article_body': article.article_body})

            save_json('articles', data)

        cat_links = ArticleCategory.objects.all()
        data = []
        for cat_link in cat_links:
            data.append(
                {'guid': cat_link.guid,
                 'article_guid': cat_link.article_guid.guid,
                 'category_guid': cat_link.category_guid.guid})

            save_json('category_links', data)

        comments = Comment.objects.all()
        data = []
        for comment in comments:
            data.append(
                {
                    'guid': comment.guid,
                    'article_uid': comment.article_uid.guid,
                    'body': comment.body,
                    'date_added': comment.date_added,
                    'time_added': comment.time_added,
                    'user_id': comment.user_id.id})

            save_json('comments', data)
