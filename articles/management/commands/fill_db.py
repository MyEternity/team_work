import datetime
import json
import random
from os import path
from random import randint

from django.core.management.base import BaseCommand

from articles.models import *
from users.models import User

JSON_PATH = 'articles/json'


def load_from_json(file_name):
    with open(path.join(JSON_PATH, file_name + '.json'), 'r') as file:
        return json.load(file)


comment_arr = [
    'Отличная статья!',
    'Хвалебная ода автору!',
    'Круто написано!',
    'Ни о чем, непонятно что да как.',
    'Много букв и куча всякой рекламы, зачем это тут?',
    'Если бы я понял о чем тут, то что-то бы и написал)',
    'Мда... кг/ам.',
    'Купите мультиварку, чуток БУ, но жарит еще по самое немогу, инфа в профиле',
    'Что курил автор?',
    'Не знаю о чем тут, но картинки красивые )))',
    'Спасибо, поржал xDDD'
]

sub_comment_arr = [
    'Вы даже не понимаете о чем пишете!',
    'Странный коммент не по теме',
    'Аффтар убейсо апстенку!',
    'Не согласен, если посмотреть на эти вещи сбоку, то спереди сзади ничего и нет!',
    'Поддерживаю'
]

usr_names = [
    'Василий',
    'Петр',
    'Савелий',
    'Иван',
    'Олеся',
    'Жанна',
    'Екатерина',
    'Иосиф'
]

# Нафигачил тут хохлов, чтобы не париться со склонениями))))
usr_surnames = [
    'Иванченко',
    'Ляпченко',
    'Петченко',
    'Ким',
    'Скайуокер',
    'Сталин',
    'Лукашенко',
    'Лукьяненко'
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        Category.objects.all().delete()
        for category in categories:
            new_category = Category(**category)
            new_category.save()

        print('Initializing users..')
        users = load_from_json('users')
        for user in users:
            usr = User.objects.filter(id=user['id'])
            if not usr:
                new_user = User(**user)
                new_user.save()
            else:
                print(f'User {usr} already exists.')

        print('Processing articles..')
        articles = load_from_json('articles')
        for article in articles:
            obj = Article.objects.filter(guid=article['guid'])
            if not obj:
                print('New article found.')
                article['author_id'] = User.objects.get(id=article["author_id"])
                article['publication'] = True
                Article(**article).save()
            else:
                obj = Article.objects.get(guid=article['guid'])
                obj.author_id = random.choice(User.objects.all())
                obj.creation_date = datetime.date(2022, random.choice(range(1, 10)), random.choice(range(1, 28)))
                print(f'Updating author to {obj.author_id} in existing article.')
                obj.save()

        print('Processing article categories..')
        ArticleCategory.objects.all().delete()
        for obj in Article.objects.all():
            for k in range(1, randint(2, 3)):
                ex_list = [x.category_guid_id for x in ArticleCategory.objects.filter(article_guid=obj.guid)]
                cat_list = Category.objects.exclude(
                    guid__in=[x.category_guid_id for x in ArticleCategory.objects.filter(article_guid=obj.guid)])
                if len(ex_list) < 2:
                    record = ArticleCategory.objects.create(article_guid=obj, category_guid=random.choice(cat_list))
                    print(f'Added new category for {record.article_guid} : {record.category_guid}')

        Notification.objects.all().delete()
        Comment.objects.all().delete()
        CommentLike.objects.all().delete()
        ArticleLike.objects.all().delete()

        print('Processing users...')
        if User.objects.all().count() < 4:
            for u in range(1, randint(8, 16)):
                User.objects.create(username=f'user_{u + 1000}', email=f'{str(uuid.uuid4()).replace("-", "")}@mail.ru',
                                    first_name=random.choice(usr_names), last_name=random.choice(usr_surnames),
                                    password="pbkdf2_sha256$390000$W9ScL6JhnkitBcoLExaSot$/xBnflk2GlA/T/HQl4K17c7lAdHi7+vHAzseDN1xhfM=")
        us = User.objects.all()
        for u in us:
            u.first_name = random.choice(usr_names)
            u.last_name = random.choice(usr_surnames)
            u.save()

        print('Processing comments and likes for articles...')
        arr_usr = [k.id for k in us]
        qs = Article.objects.all()
        for a in qs:
            for k in range(1, randint(8, 12)):
                Comment.objects.create(article_uid=a, body=random.choice(comment_arr),
                                       user_id=User.objects.get(id=random.choice(arr_usr)))
            for k in range(1, randint(8, 11)):
                ArticleLike.set_like(article=a, user=random.choice(us))

        print('Processing likes for comments...')
        qs = Comment.objects.all()
        for c in qs:
            for k in range(2, randint(3, 8)):
                CommentLike.set_like(comment=c, user=random.choice(us))

        print('Creating sub_comments...')
        for c in Comment.objects.all():
            for _ in [0, 1, 2]:
                if random.choice([True, False, False, True, False, False, False, True]):
                    usr_arr = [u.id for u in User.objects.exclude(id=c.user_id.id)]
                    CommentComment.objects.create(comment_uid=c, user_id=User.objects.get(id=random.choice(usr_arr)),
                                                  body=random.choice(sub_comment_arr))

        print('Everything is up to date!')
