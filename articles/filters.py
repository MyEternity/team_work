from .models import Article
from django_filters import CharFilter, FilterSet
from django.db.models import Q


class ArticleFilter(FilterSet):
    search = CharFilter(method='custom_filter', label="Поиск по статьям:")

    class Meta:
        model = Article
        fields = ['search']

    def custom_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(article_body__icontains=value) | Q(topic__icontains=value))
        return queryset
