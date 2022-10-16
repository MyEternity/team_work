from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Article, ArticleHistory, Category, ArticleCategory


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('article_body',)


admin.site.register(Article, PostAdmin)
admin.site.register(ArticleHistory)
admin.site.register(ArticleCategory)
admin.site.register(Category)
