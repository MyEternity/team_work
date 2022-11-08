from django.db.models import Q, Sum
from django.forms.widgets import TextInput, Select
from django_filters import CharFilter, FilterSet, ChoiceFilter

from .models import Article

CHOICES = (
    ('new', 'Сначала новые'),
    ('old', 'Сначала старые'),
    ('most', 'Сначала популярные'),
    ('least', 'Сначала непопулярные')
)


class ArticleFilter(FilterSet):
    text = CharFilter(method='text_filter', label='Поиск по содержанию статьи:',
                      widget=TextInput(attrs={'placeholder': 'Текст'}))

    ordering = ChoiceFilter(choices=CHOICES, method='ordering_filter',
                            label='Сортировка:',
                            widget=Select(attrs={'placeholder': 'Сортировка'}))

    class Meta:
        model = Article
        fields = ['ordering', 'text']

    def text_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(article_body__icontains=value) | Q(topic__icontains=value))
        return queryset

    def ordering_filter(self, queryset, name, value):
        field_choices = {
            'new': '-creation_date',
            'old': 'creation_date',
            'most': '-likes',
            'least': 'likes'
        }

        field = field_choices.get(value, 0)

        if field:
            queryset = queryset.annotate(likes=Sum('articlelike__event_counter')).order_by(field)
        return queryset
