from django.db.models import Q
from django.forms.widgets import TextInput
from django_filters import CharFilter, FilterSet

from .models import Article


class ArticleFilter(FilterSet):
    search = CharFilter(method='custom_filter', label='', widget=TextInput(attrs={'placeholder': 'Поиск'}))

    class Meta:
        model = Article
        fields = ['search']

    def custom_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(article_body__icontains=value) | Q(topic__icontains=value))
        return queryset
