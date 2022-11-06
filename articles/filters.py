from django.db.models import Q, Sum
from django.forms.widgets import TextInput, Select
from django_filters import CharFilter, FilterSet, ChoiceFilter

from .models import Article, ArticleLike

DATE_CHOICES = (
    ('new', 'Сначала новые'),
    ('old', 'Сначала старые')
)

RATING_CHOICES = (
    ('most', 'Сначала популярные'),
    ('least', 'Сначала непопулярные')
)


def get_likes_count(article_guid):
    counter = ArticleLike.objects.filter(article_uid=article_guid).aggregate(Sum('event_counter')).get(
        'event_counter__sum', 0)
    return "0" if counter is None else str(counter)


class ArticleFilter(FilterSet):
    date = ChoiceFilter(choices=DATE_CHOICES, method='date_ordering_filter',
                        label='По дате публикации:',
                        widget=Select(attrs={'placeholder': 'Дата'}))

    rating = ChoiceFilter(choices=RATING_CHOICES, method='rating_ordering_filter',
                          label='По рейтингу:',
                          widget=Select(attrs={'placeholder': 'Рейтинг'}))

    text = CharFilter(method='text_filter', label='', widget=TextInput(attrs={'placeholder': 'Текст'}))

    class Meta:
        model = Article
        fields = ['rating', 'date', 'text']

    def date_ordering_filter(self, queryset, name, value):
        value = value
        match value:
            case 'new':
                queryset = queryset.order_by('-creation_date')
            case 'old':
                queryset = queryset.order_by('creation_date')
        return queryset

    def rating_ordering_filter(self, queryset, name, value):
        value = value
        match value:
            case 'most':
                queryset = queryset.annotate(likes=Sum('articlelike__event_counter')).order_by('-likes')
            case 'least':
                queryset = queryset.annotate(likes=Sum('articlelike__event_counter')).order_by('likes')
        return queryset

    def text_filter(self, queryset, name, value):
        value = value
        queryset = queryset.filter(Q(article_body__icontains=value) | Q(topic__icontains=value))
        return queryset
