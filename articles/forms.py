from django import forms
from .models import Article
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ArticleAddUpdateDeleteForm(forms.ModelForm):
    """
    класс для создания, редактирования и удаления нового поста
    """
    article_body = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Article
        fields = ('author_id', 'topic', 'article_body')
