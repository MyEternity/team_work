from .models import Article
from django_filters import CharFilter, FilterSet
from django.db.models import Q


class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = ['topic']

    topic = CharFilter(field_name='topic', lookup_expr='icontains', label='Поиск по названию статьи:')

# class ArticleFilter(FilterSet):
#     q = CharFilter(method='custom_filter', label="Поиск по статьям:")
#
#     class Meta:
#         model = Article
#         fields = ['q']
#
#     def custom_filter(self, queryset, name, value):
#         queryset = queryset.filter(Q(topic__icontains=value), Q(article_body__icontains=value))
#         return queryset
