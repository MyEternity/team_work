from django.db.models import Sum

from articles.models import ArticleLike, Article


def count_rating(user_id):
    counter = 0
    articles = Article.objects.filter(author_id=user_id).order_by('guid')
    for guid in articles:
        counter = ArticleLike.objects.filter(article_uid_id=guid).aggregate(Sum('event_counter'))
    print(counter)
    return counter

