
from django.views.generic import FormView
from django.views.generic import FormView, CreateView, UpdateView, DetailView, TemplateView, DeleteView, ListView
from .forms import ArticleAddUpdateDeleteForm
from django.urls import reverse_lazy


from articles.models import Article
import re


class IndexListView(ListView):
    """Класс IndexListView - для вывода статей на главной страницы."""
    paginate_by = 10
    model = Article
    title = 'Articles-Krabr'
    # Шаблона еще нет, делаю на базоый шаблон.
    template_name = 'articles/articles_list.html'

    def get_queryset(self):
        # Сортировка - сверху новые.
        qs = Article.objects.all().prefetch_related('author_id').\
            order_by('-creation_date')
        # По совета Андрея вывожу только первый параграф. Редактор сохраняет
        # параграф в тег <p>. По этому обезаю по первому тегу.
        # Отдаю чистую строку без тегов.
        # Потом надо будет решить вопрос или оставить так, если подойдёт.
        for q in qs:
            # Проверка, что в статье больше одного параграфа.
            if len(re.findall('<.*?>', q.article_body)) > 2:
                q.article_body = re.sub('<.>\w*<..>', '', q.article_body)
                q.article_body = re.sub('<.*?>', '', q.article_body)
            else:
                q.article_body = re.sub('<.*?>', '', q.article_body)
        return qs

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        return context


class CreateArticleView(CreateView):
    """
    заготовка для проверки работы форм
    """
    model = Article
    title = 'Добавить пост'
    form_class = ArticleAddUpdateDeleteForm
    template_name = 'articles/add_post.html'
    success_url = reverse_lazy('articles:index')


class UpdateArticleView(UpdateView):
    model = Article
    title = 'Редактировать пост'
    form_class = ArticleAddUpdateDeleteForm
    template_name = 'articles/add_post.html'
    success_url = reverse_lazy('articles:index')


# удаление нужно?
class DeleteArticleView(DeleteView):
    model = Article
    title = 'Удалить пост'
    form_class = ArticleAddUpdateDeleteForm
    template_name = 'articles/add_post.html'
    success_url = reverse_lazy('articles:index')


class ArticleDetailView(DetailView):
    """Класс ArticleDetailView - для вывода одной статьи."""
    model = Article
    title = 'Article'
    # В качестве слага передавать - guid.
    slug_field = 'guid'
    # В шаблон будет передана пеменная с именем - article.
    context_object_name = 'article'
    # Шаблона еще нет...
    template_name = ''
