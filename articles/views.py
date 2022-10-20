from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import FormView, CreateView, UpdateView, DetailView, TemplateView, DeleteView, ListView

from team_work.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from .forms import ArticleAddUpdateDeleteForm
from .filters import ArticleFilter
from .models import Comment
from django.urls import reverse_lazy
from bs4 import BeautifulSoup

from articles.models import Article, Category, Notification


class IndexListView(BaseClassContextMixin, ListView):
    """Класс IndexListView - для вывода статей на главной страницы."""

    paginate_by = 3
    model = Article
    articles_filtered = None
    title = 'Крабр - Лучше, чем Хабр'
    template_name = 'articles/articles_list.html'

    def get_queryset(self):
        img_height = '400px'

        # Сортировка, сверху - новые
        qs = Article.objects.all().prefetch_related('author_id'). \
            order_by('-articlehistory__record_date')

        # Фильтрация по поиску
        self.articles_filtered = ArticleFilter(self.request.GET, queryset=qs)

        # Работа с preview
        for article in self.articles_filtered.qs:
            preview_p = ''
            new_article_body = ''

            soup = BeautifulSoup(article.article_body, 'html.parser')

            preview_img = soup.img
            # Стилизация изображения под ограничение высоты, центрирование
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
        return self.articles_filtered.qs

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        context["filter"] = self.articles_filtered
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

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(article_uid=self.kwargs['slug'])
        return context


class CategoryView(BaseClassContextMixin, ListView):
    model = Article
    template_name = 'articles/category.html'
    context_object_name = 'articles'

    def get_queryset(self):
        self.category = get_object_or_404(Category, guid=self.kwargs['slug'])
        self.title = self.category.name
        queryset = Article.objects.filter(articlecategory__category_guid=self.kwargs['slug'])

        return queryset


class NotificationListView(BaseClassContextMixin, UserLoginCheckMixin,
                           ListView):
    """Класс NotificationListView - для вывода уведомлений пользователя."""
    paginate_by = 20
    model = Notification
    title = 'Уведомления'
    template_name = 'articles/notifications.html'

    def get_queryset(self, **kwargs):
        qs = Notification.objects.filter(recipient_id=self.request.user.id)\
            .prefetch_related('author_id')
        return qs


def notification_readed(request, slug):
    """Функция-ajax для обновления данных из таблицы уведомлений."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        notification = Notification.objects.get(guid=slug)
        if notification.message_readed:
            notification.message_readed = False
        else:
            notification.message_readed = True
        notification.save()

        object_list = Notification.objects\
            .filter(recipient_id=request.user.id)\
            .prefetch_related('author_id')
        context = {'object_list': object_list}
        result = render_to_string('articles/includes/table_notifications.html',
                                  context)
        return JsonResponse({'result': result})
