from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView, UpdateView, DetailView, TemplateView, DeleteView, ListView

from team_work.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from .forms import ArticleAddUpdateDeleteForm
from django.urls import reverse_lazy
from bs4 import BeautifulSoup

from articles.models import Article


class IndexListView(BaseClassContextMixin, ListView):
    """Класс IndexListView - для вывода статей на главной страницы."""
    paginate_by = 3
    model = Article
    title = 'Крабр - Лучше, чем Хабр'
    # Шаблона еще нет, делаю на базоый шаблон.
    template_name = 'articles/articles_list.html'

    def get_queryset(self):
        img_height = '400px'

        # Сортировка - сверху новые.
        qs = Article.objects.all().prefetch_related('author_id'). \
            order_by('-articlehistory__record_date')

        for article in qs:
            preview_p = ''
            new_article_body = ''

            soup = BeautifulSoup(article.article_body, 'html.parser')

            preview_img = soup.img
            # Стилизация изображения под ограничение ширины, центрирование
            if preview_img:
                preview_img['style'] = f'height: {img_height}; object-fit: scale-down; float: none;' \
                                       f' display: block; margin-left: auto; margin-right: auto;'
                new_article_body += str(preview_img)

            # Поиск первого существенного абзаца
            p_lst = soup.find_all('p')
            for p in p_lst:
                if p.text:
                    if p.img:
                        p.img.decompose()
                    preview_p = p
                    break
            new_article_body += str(preview_p)

            article.article_body = new_article_body
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
