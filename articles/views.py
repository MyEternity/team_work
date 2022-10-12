from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView, UpdateView, DetailView, TemplateView, DeleteView, ListView

from team_work.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from .forms import ArticleAddUpdateDeleteForm
from django.urls import reverse_lazy


from articles.models import Article
import re


class IndexListView(BaseClassContextMixin, ListView):
    """Класс IndexListView - для вывода статей на главной страницы."""
    paginate_by = 3
    model = Article
    title = 'Крабр - Лучше, чем Хабр'
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
        # for q in qs:
        #     # Проверка, что в статье больше одного параграфа.
        #     if len(re.findall('<.*?>', q.article_body)) > 2:
        #         q.article_body = re.sub('<.>\w*<..>', '', q.article_body)
        #         q.article_body = re.sub('<.*?>', '', q.article_body)
        #     else:
        #         q.article_body = re.sub('<.*?>', '', q.article_body)
        return qs

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        return context


class CreateArticleView(BaseClassContextMixin, UserLoginCheckMixin, CreateView):
    model = Article
    title = 'Добавить статью'
    form_class = ArticleAddUpdateDeleteForm
    template_name = 'articles/add_post.html'
    success_url = reverse_lazy('articles:index')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = ArticleAddUpdateDeleteForm(data=request.POST)
        form.instance.author_id = self.request.user
        if form.is_valid():
            form.save()
        return redirect(self.success_url)


class UpdateArticleView(BaseClassContextMixin, UserLoginCheckMixin, UpdateView):
    model = Article
    title = 'Редактировать статью'
    form_class = ArticleAddUpdateDeleteForm
    template_name = 'articles/add_post.html'
    success_url = reverse_lazy('articles:index')


# удаление нужно?
class DeleteArticleView(BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin, DeleteView):
    model = Article
    title = 'Удалить статью'
    form_class = ArticleAddUpdateDeleteForm
    template_name = 'articles/add_post.html'
    success_url = reverse_lazy('articles:index')


class ArticleDetailView(BaseClassContextMixin, DetailView):
    """Класс ArticleDetailView - для вывода одной статьи."""
    model = Article
    title = 'Статья'
    # В качестве слага передавать - guid.
    slug_field = 'guid'
    # В шаблон будет передана пеменная с именем - article.
    context_object_name = 'article'
    # Шаблона еще нет...
    template_name = ''
