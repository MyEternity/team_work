from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'
    verbose_name = 'Статьи и публикации'


class SummernoteConfig(AppConfig):
    verbose_name = 'Вложения'