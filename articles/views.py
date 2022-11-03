from bs4 import BeautifulSoup
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.defaultfilters import truncatechars_html
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView

from articles.models import Article, Category, Notification
from team_work.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin, ArticleSearchMixin
from users.models import User
from .filters import ArticleFilter
from .forms import ArticleAddUpdateDeleteForm, CommentForm, SelectCategoryForm
from .models import Comment, ArticleCategory, ArticleLike


def preview_handler(queryset, max_preview_chars):
    """
    Функция принимает query set и максимальное количество символов в итоговом preview
    Результат работы функции - обработанный query set
    """
    for article in queryset:
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


class IndexListView(BaseClassContextMixin, ArticleSearchMixin, ListView):
    """Класс IndexListView - для вывода статей на главной страницы."""

    paginate_by = 5
    model = Article
    title = 'Крабр - Лучше, чем Хабр'
    template_name = 'articles/articles_list.html'

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        preview_handler(context["object_list"], 400)
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
        context['categories'] = SelectCategoryForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ArticleAddUpdateDeleteForm(data=request.POST)
        form_article_category = SelectCategoryForm(data=request.POST)
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
    slug_field = 'guid'
    form_class = ArticleAddUpdateDeleteForm
    template_name = 'articles/add_post.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Article, pk=self.kwargs['slug'])

    @transaction.atomic
    def get_context_data(self, **kwargs):
        context = super(UpdateArticleView, self).get_context_data(**kwargs)
        context['categories_checked'] = ArticleCategory.objects.filter(article_guid=self.kwargs['slug']).values_list(
            'category_guid', flat=True)
        context['categories'] = SelectCategoryForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ArticleAddUpdateDeleteForm(data=request.POST, instance=self.get_object())
        form_article_category = SelectCategoryForm(data=request.POST)
        form.instance.author_id = self.request.user
        if form.is_valid() and form_article_category.is_valid():
            form.save()
            ArticleCategory.objects.filter(article_guid=self.kwargs['slug']).delete()
            for cat in Category.objects.filter(
                    guid__in=[x for x in form.data.getlist('name')]):
                ArticleCategory.objects.create(
                    article_guid=Article.objects.get(guid=self.kwargs['slug']),
                    category_guid=cat)
            return redirect(reverse_lazy('articles:article-detail',
                                         kwargs={'slug': self.kwargs["slug"]}))
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Выберите хотя бы одну категорию.")
            return render(request,
                          self.template_name,
                          {'form': form, 'categories': form_article_category})


# удаление нужно?
class DeleteArticleView(BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin, DeleteView):
    model = Article
    title = 'Удалить статью'
    success_url = reverse_lazy('articles:index')

    def get_object(self, queryset=None):
        return get_object_or_404(Article, guid=self.kwargs['slug'])


class ArticleDetailView(BaseClassContextMixin, DetailView):
    """Класс ArticleDetailView - для вывода одной статьи."""
    model = Article
    title = 'Статья'
    slug_field = 'guid'
    context_object_name = 'article'
    template_name = 'articles/view_post.html'
    form_class = CommentForm

    def __init__(self, **kwargs):
        super(ArticleDetailView, self).__init__(**kwargs)
        self.object = None
        self.is_ajax = False

    def post(self, request, *args, **kwargs):
        self.is_ajax = True if request.headers.get('X-Requested-With') == 'XMLHttpRequest' else False
        _post = request.POST.copy()
        _post['article_uid'] = Article.objects.get(guid=kwargs.get('slug', None))
        form = self.form_class(data=_post)
        if form.is_valid() and self.is_ajax:
            self.object = Comment.objects.create(article_uid=_post['article_uid'], body=_post['body'],
                                                 user_id=request.user)
            if self.object.body.find('@moderator'):
                for u in User.objects.filter(is_staff=True, is_active=True):
                    if u != request.user:
                        Notification.objects.create(author_id=request.user, recipient_id=u,
                                                    article_uid=_post['article_uid'],
                                                    message='взывает к чистоте и порядку: ')
            return JsonResponse(
                {'result': 1, 'object': f'c_{kwargs.get("slug", None)}', 'like_object': f'{kwargs.get("slug", None)}',
                 'data': render_to_string('articles/includes/article_comments.html',
                                          {'comments': Comment.objects.filter(article_uid=self.kwargs['slug']),
                                           'article': _post['article_uid']}),
                 'like': render_to_string('articles/includes/article_bottom.html',
                                          {'article': _post['article_uid'], 'request': request, 'user': request.user})})
        else:
            if self.is_ajax:
                return JsonResponse({'result': 1, 'errors': form.errors})
        return redirect(reverse_lazy('articles:article-detail', kwargs={'slug': self.get_object().pk}))

    def get_context_data(self, **kwargs):
        article_comments = Comment.objects.filter(article_uid=self.kwargs['slug'])
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        # context['comments'] = Comment.objects.filter(article_uid=self.kwargs['slug'])
        context.update({
            'form': self.form_class,
            'comments': article_comments,
        })
        return context


class CategoryView(BaseClassContextMixin, ArticleSearchMixin, ListView):
    model = Article
    paginate_by = 6
    template_name = 'articles/category.html'
    context_object_name = 'articles'

    def __init__(self, **kwargs):
        super(CategoryView, self).__init__(**kwargs)
        self.category = None

    def get_queryset(self, **kwargs):
        self.queryset = super(CategoryView, self).get_queryset()
        self.category = get_object_or_404(Category, guid=self.kwargs['slug'])
        self.title = self.category.name
        return self.queryset.filter(
            guid__in=[s.article_guid_id for s in ArticleCategory.objects.filter(category_guid=self.category)])

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        preview_handler(context["object_list"], 400)
        return context


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

        object_list = Notification.objects.filter(recipient_id=request.user.id).prefetch_related('author_id')[:20]
        context = {'object_list': object_list}
        result = render_to_string('articles/includes/table_notifications.html',
                                  context)
        return JsonResponse({'result': result})


def like_pressed(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        a = Article.objects.get(guid=request.POST['article'])
        ArticleLike.set_like(a, request.user)
        return JsonResponse(
            {'result': 1, 'object': a.guid,
             'data': render_to_string('articles/includes/article_bottom.html',
                                      {'article': a, 'request': request, 'user': request.user})})


class AuthorArticles(BaseClassContextMixin, ArticleSearchMixin, ListView):
    """
    Класс выводит статьи от запрошенного пользователя
    """
    model = Article
    title = 'Статьи пользователя'
    template_name = 'articles/articles_list.html'
    slug_field = 'author_id'

    def get_queryset(self, **kwargs):
        queryset = super(AuthorArticles, self).get_queryset()
        queryset.filter(author_id=self.kwargs['slug'])

        preview_handler(self.articles_filtered.qs, 100)
        return queryset
