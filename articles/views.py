from django.views.generic import FormView
from django.views.generic import FormView, CreateView, UpdateView, DetailView, TemplateView, DeleteView
from .forms import ArticleAddUpdateDeleteForm
from .models import Article


# Create your views here.


class IndexView(FormView):
    title = 'Добро пожаловать на Хабр!'
    form_class = FormView
    template_name = 'articles/articles_list.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class CreatePostView(CreateView):
    """
    заготовка для проверки работы форм
    """
    model = Article
    title = 'Добавить пост'
    form_class = ArticleAddUpdateDeleteForm
    template_name = 'articles/add_post.html'


class UpdatePostView(UpdateView):
    model = Article
    title = 'Редактировать пост'
    form_class = ArticleAddUpdateDeleteForm
    template_name = 'articles/add_post.html'


# удаление нужно?
class DeletePostView(DeleteView):
    model = Article
    title = 'Редактировать пост'
    form_class = ArticleAddUpdateDeleteForm
    template_name = 'articles/add_post.html'
