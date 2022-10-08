from django.urls import path

from .views import ArticleDetailView

app_name = 'articles'

urlpatterns = [
    path('article/<slug:slug>/', ArticleDetailView.as_view(),
         name='article-detail'),
]
