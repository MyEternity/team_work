from django.urls import path


from .views import IndexListView, CreateArticleView, UpdateArticleView, DeleteArticleView, ArticleDetailView, SearchResultsView


app_name = 'articles'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('add_post/', CreateArticleView.as_view(), name='add_post'),
    path('update_post/', UpdateArticleView.as_view(), name='update_post'),
    path('delete_post/', DeleteArticleView.as_view(), name='delete_post'),  # убрать если не нужен
    path('article/<slug:slug>/', ArticleDetailView.as_view(),
         name='article-detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
