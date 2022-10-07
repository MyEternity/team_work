from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView


# Create your views here.


class IndexView(FormView):
    title = 'Добро пожаловать на Хабр!'
    form_class = FormView
    template_name = 'articles/articles_list.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context
