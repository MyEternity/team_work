from collections import Counter

from django.db.models import Sum

from articles.models import ArticleLike, Article, Comment, CommentLike


def user_rating(user_id):
    # user_rating возвращает число соотвествующее общему количеству лайков
    # которые были поставлены пользователю под статьями и комментариями
    object_list = []
    articles = Article.objects.filter(author_id=user_id)  # получаем guid всех статей автора

    for guid in articles:  # собираем сумму все лайки ко всем статьям
        object_list.append(ArticleLike.objects.filter(article_uid_id=guid).aggregate(Sum('event_counter')))

    comments = Comment.objects.filter(user_id=user_id)  # получаем guid всех комментариев автора

    for guid in comments:  # собираем сумму все лайки ко всем комментам
        object_list.append(CommentLike.objects.filter(comment_uid=guid).aggregate(Sum('event_counter')))

    counter = Counter({'event_counter__sum': 0})
    for value in object_list:  # считаем лайки
        counter += Counter(value)

    return counter['event_counter__sum']


# следующие три функции нигде не используются, но с их помощью можно добавить множители рейтинга для статей
def count_articles_likes(user_id):
    # функция считает лайки за статьи
    object_list = []
    articles = Article.objects.filter(author_id=user_id)  # получаем guid всех статей автора
    for guid in articles:  # собираем сумму все лайки ко всем статьям
        object_list.append(ArticleLike.objects.filter(article_uid_id=guid).aggregate(Sum('event_counter')))
    counter = Counter({'event_counter__sum': 0})
    for value in object_list:  # считаем лайки
        counter += Counter(value)
    return counter


def count_comments_likes(user_id):
    # функция считает лайки за комменты
    object_list = []
    comments = Comment.objects.filter(user_id=user_id)  # получаем guid всех комментариев автора
    for guid in comments:  # собираем сумму все лайки ко всем комментам
        object_list.append(CommentLike.objects.filter(comment_uid=guid).aggregate(Sum('event_counter')))
    counter = Counter({'event_counter__sum': 0})
    for value in object_list:  # считаем лайки
        counter += Counter(value)
    return counter


def total_rating(user_id):
    # функция складывает лайки за статьи и комментарии
    # при необходимости тут можно добавлять множители
    total = count_articles_likes(user_id) + count_comments_likes(user_id)
    return total['event_counter__sum']
