from django import template
from django.template.defaultfilters import stringfilter

from articles.models import Comment, ArticleLike

register = template.Library()


@register.filter
def rm_obs_pages(data):
    if 'page' in data:
        data._mutable = True
        data.pop('page')
        data._mutable = False
    return data.urlencode()


@register.filter
@stringfilter
def get_comments_count(article_guid):
    return str(Comment.count(article_guid))


@register.filter
@stringfilter
def get_likes_count(article_guid):
    return str(ArticleLike.count(article_guid))
