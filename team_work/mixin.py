from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import ContextMixin

from articles.models import Category, Article
from articles.filters import ArticleFilter


class UserIsAdminCheckMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserIsAdminCheckMixin, self).dispatch(request, *args, **kwargs)


class UserIsModeratorCheckMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return super(UserIsModeratorCheckMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed(request.method)


class UserLoginCheckMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            return super(UserLoginCheckMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed(request.method)


class BaseClassContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(BaseClassContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['menu_links'] = Category.objects.filter(is_active=True)
        return context


class ArticleSearchMixin(ContextMixin):
    def __init__(self):
        self.request = None
        self.articles_filtered = None

    def get_queryset(self):
        qs = Article.objects.filter(blocked=False)
        self.articles_filtered = ArticleFilter(self.request.GET, queryset=qs)
        return self.articles_filtered.qs

    def get_context_data(self, **kwargs):
        context = super(ArticleSearchMixin, self).get_context_data(**kwargs)
        context['filter'] = self.articles_filtered
        return context
