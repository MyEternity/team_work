import json
import random
from os import path
from random import randint
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
        for user in users:
            if not User.objects.get(id=user['id']):
                new_user = User(**user)
                new_user.save()
            else:
                print(f'User {user["id"]} already exists.')

        articles = load_from_json('articles')
        for article in articles:
            obj = Article.objects.get(guid=article['guid'])
            if not obj:
                print('New article found.')
                article['author_id'] = User.objects.get(id=article["author_id"])
                Article(**article).save()
            else:
                obj.author_id = random.choice(User.objects.all())
                print(f'Updating author to {obj.author_id} in existing article.')
                obj.save()

        ArticleCategory.objects.all().delete()
        for obj in Article.objects.all():
            for k in range(1, randint(1, 3)):
                ex_list = [x.category_guid_id for x in ArticleCategory.objects.filter(article_guid=obj.guid)]
                cat_list = Category.objects.exclude(
                    guid__in=[x.category_guid_id for x in ArticleCategory.objects.filter(article_guid=obj.guid)])
                if len(ex_list) < 2:
                    record = ArticleCategory.objects.create(article_guid=obj, category_guid=random.choice(cat_list))
                    print(f'Added new category for {record.article_guid} : {record.category_guid}')
