from django.views.generic import ListView, DetailView

from articles.models import Article
import re


class IndexListView(ListView):
    """Класс IndexListView - для вывода статей на главной страницы."""
    paginate_by = 10
    model = Article
    # Шаблона еще нет, делаю на базоый шаблон.
    template_name = 'base.html'

    def get_queryset(self):
        # Сортировка - сверху новые.
        qs = Article.objects.all().prefetch_related('author_id').\
            order_by('-creation_date')
        # По совета Андрея вывожу только первый параграф. Редактор сохраняет
        # параграф в тег <p>. По этому обезаю по первому тегу.
        # Отдаю чистую строку без тегов.
        # Потом надо будет решить вопрос или оставить так, если подойдёт.
        for q in qs:
            q.article_body = re.sub('<.>\w*<..>', '', q.article_body)
            q.article_body = re.sub('<.*?>', '', q.article_body)
        return qs


class ArticleDetailView(DetailView):
    """Класс ArticleDetailView - для вывода одной статьи."""
    model = Article
    # В качестве слага передавать - guid.
    slug_field = 'guid'
    # В шаблон будет передана пеменная с именем - article.
    context_object_name = 'article'
    # Шаблона еще нет...
    template_name = ''
