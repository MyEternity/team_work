from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from django.template.defaultfilters import truncatechars_html

from team_work.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from .forms import ArticleAddUpdateDeleteForm, ArticleCategoryForm
from .filters import ArticleFilter
from .models import Comment, ArticleCategory
from django.urls import reverse_lazy
from bs4 import BeautifulSoup

from articles.models import Article, Category, Notification


def preview_handler(filtered_qs, max_preview_chars):
    """
    Функция принимает query set и максимальное количесво символов в итоговом preview
    Результат работы функции - обработанный query set
    """
    for article in filtered_qs:
        article_body = BeautifulSoup(article.article_body, 'html.parser')
        new_article_body = ''

        first_img = article_body.img

        # Обнуляем стиль preview изображения и размещаем в начале preview
        if first_img:
            first_img['class'] = "preview_img"
            del first_img['style']
            new_article_body += str(first_img)

        # Удаляем все лишние изображения
        while article_body.img:
            article_body.img.decompose()

        # Обрезаем preview text
        new_body = truncatechars_html(article_body, max_preview_chars)
        new_article_body += new_body
        article.article_body = new_article_body


class IndexListView(BaseClassContextMixin, ListView):
    """Класс IndexListView - для вывода статей на главной страницы."""

    paginate_by = 8
    model = Article
    articles_filtered = None
    title = 'Крабр - Лучше, чем Хабр'
    template_name = 'articles/articles_list.html'

    def get_queryset(self):
        # Сортировка, сверху - новые
        qs = Article.objects.all().prefetch_related('author_id'). \
            order_by('-articlehistory__record_date')

        self.articles_filtered = ArticleFilter(self.request.GET, queryset=qs)

        preview_handler(self.articles_filtered.qs, 400)

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
    def get_context_data(self, **kwargs):
        context = super(CreateArticleView, self).get_context_data(**kwargs)
        context['categories'] = ArticleCategoryForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ArticleAddUpdateDeleteForm(data=request.POST)
        form_article_category = ArticleCategoryForm(data=request.POST)
        form.instance.author_id = self.request.user
        if form.is_valid() and form_article_category.is_valid():
            form.save()
            for cat in Category.objects.filter(
                    guid__in=[x for x in form.data.getlist('name')]):
                ArticleCategory.objects.create(
                    article_guid=Article.objects.get(guid=form.instance.guid),
                    category_guid=cat)
            return redirect(self.success_url)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Выберите хотя бы одну категорию.")
            return render(request,
                      self.template_name,
                      {'form': form, 'categories': form_article_category})


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
        qs = Notification.objects.filter(recipient_id=self.request.user.id) \
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

        object_list = Notification.objects \
            .filter(recipient_id=request.user.id) \
            .prefetch_related('author_id')
        context = {'object_list': object_list}
        result = render_to_string('articles/includes/table_notifications.html',
                                  context)
        return JsonResponse({'result': result})


class AuthorArticles(BaseClassContextMixin, ListView):
    """
    класс выводит статьи от запрошенного пользователя
    """
    model = Article
    articles_filtered = None
    title = 'Статьи пользователя'
    template_name = 'articles/articles_list.html'
    slug_field = 'author_id'

    def get_queryset(self, **kwargs):
        qs = Article.objects.filter(author_id=self.kwargs['slug'])

        self.articles_filtered = ArticleFilter(self.request.GET, queryset=qs)

        preview_handler(self.articles_filtered.qs, 100)

        return self.articles_filtered.qs
