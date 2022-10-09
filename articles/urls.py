from django.urls import path

from .views import IndexView, CreateArticleView, UpdateArticleView, DeleteArticleView

app_name = 'articles'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add_post/', CreateArticleView.as_view(), name='add_post'),
    path('update_post/', UpdateArticleView.as_view(), name='update_post'),
    path('delete_post/', DeleteArticleView.as_view(), name='delete_post'),  # убрать если не нужен
]
