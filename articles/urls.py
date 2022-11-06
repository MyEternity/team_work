from django.urls import path

from .views import IndexListView, CreateArticleView, UpdateArticleView, \
    DeleteArticleView, ArticleDetailView, CategoryView, NotificationListView, \
    notification_readed, AuthorArticles, like_pressed, publish_post, \
    ArticlesUserListView

app_name = 'articles'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('add_post/', CreateArticleView.as_view(), name='add_post'),
    path('update_post/<slug:slug>/', UpdateArticleView.as_view(), name='update_post'),
    path('delete_post/<slug:slug>/', DeleteArticleView.as_view(), name='delete_post'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(),
         name='article-detail'),
    path('articles_user/<int:pk>/', ArticlesUserListView.as_view(), name='articles_user'),
    path('publish_post/<slug:article_guid>/<slug:url>/', publish_post, name='publish_post'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/read/<slug:slug>/', notification_readed, name='notification_read'),
    path('likepress/', like_pressed, name='like_dislike'),
    path('user_articles/<slug:slug>/', AuthorArticles.as_view(), name='user_articles'),
]
