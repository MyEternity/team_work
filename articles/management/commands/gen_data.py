import random
import uuid
from random import randint

from django.core.management.base import BaseCommand
from django.db.models import Max

from articles.models import Article, ArticleLike, Comment, CommentLike, Notification
from users.models import User

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

usr_names = [
    'Василий',
    'Петр',
    'Савелий',
    'Иван',
    'Олеся',
    'Жанна',
    'Екатерина'
]

# Нафигачил тут хохлов, чтобы не париться со склонениями)
usr_surnames = [
    'Иванченко',
    'Ляпченко',
    'Петченко',
    'Ким',
    'Скайуокер'
]


class Command(BaseCommand):
    def handle(self, *args, **options):

        Notification.objects.all().delete()
        Comment.objects.all().delete()
        CommentLike.objects.all().delete()
        ArticleLike.objects.all().delete()

        if User.objects.all().count() < 4:
            for u in range(1, randint(8, 16)):
                User.objects.create(username=f'user_{u + 1000}', email=f'{str(uuid.uuid4()).replace("-", "")}@mail.ru',
                                    first_name=random.choice(usr_names), last_name=random.choice(usr_surnames),
                                    password="pbkdf2_sha256$390000$W9ScL6JhnkitBcoLExaSot$/xBnflk2GlA/T/HQl4K17c7lAdHi7+vHAzseDN1xhfM=")
        us = User.objects.all()
        arr_usr = [k.id for k in us]
        qs = Article.objects.all()
        for a in qs:
            for k in range(1, randint(8, 12)):
                Comment.objects.create(article_uid=a, body=random.choice(comment_arr),
                                       user_id=User.objects.get(id=random.choice(arr_usr)))
            for k in range(1, randint(4, 9)):
                ArticleLike.objects.create(article_uid=a, event_type=random.choice(['Нравится', 'Не нравится']),
                                           user_id=User.objects.get(id=random.choice(arr_usr)))
        qs = Comment.objects.all()
        for c in qs:
            for k in range(2, randint(3, 8)):
                CommentLike.objects.create(comment_uid=c, event_type=random.choice(['Нравится', 'Не нравится']),
                                           user_id=User.objects.get(id=random.choice(arr_usr)))
        print('Bulked data written)))')
