from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView, CreateView, UpdateView, DetailView, TemplateView, DeleteView, ListView

from team_work.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from .forms import ArticleAddUpdateDeleteForm
from django.urls import reverse_lazy
from bs4 import BeautifulSoup

from articles.models import Article, Category


class IndexListView(BaseClassContextMixin, ListView):
    """Класс IndexListView - для вывода статей на главной страницы."""
    paginate_by = 5
    model = Article
    title = 'Крабр - Лучше, чем Хабр'
    # Шаблона еще нет, делаю на базоый шаблон.
    template_name = 'articles/articles_list.html'

    def get_queryset(self):
        preview_p = None
        # Сортировка - сверху новые.
        qs = Article.objects.all().prefetch_related('author_id'). \
            order_by('-articlehistory__record_date')
        # Парсинг в поисках первого тега и изображения
        for article in qs:
            soup = BeautifulSoup(article.article_body, 'html.parser')
            preview_img = soup.img
            p_lst = soup.find_all('p')
            for p in p_lst:
                if p.text:
                    preview_p = p
                    break
            if preview_img:
                article.article_body = str(preview_img) + str(preview_p)
            else:
                article.article_body = str(preview_p)
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
    slug_field = 'guid'
    context_object_name = 'article'
    template_name = 'articles/view_post.html'


class CategoryView(BaseClassContextMixin, ListView):
    model = Article
    template_name = 'articles/category.html'
    context_object_name = 'articles'

    def get_queryset(self):
        self.category = get_object_or_404(Category, guid=self.kwargs['slug'])
        self.title = self.category.name
        queryset = Article.objects.filter(articlecategory__category_guid=self.kwargs['slug'])

        return queryset
