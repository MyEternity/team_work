from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Article


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('article_body',)


admin.site.register(Article, PostAdmin)
