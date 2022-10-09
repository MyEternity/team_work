from django import forms
from .models import Article
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ArticleAddUpdateDeleteForm(forms.ModelForm):
    """
    класс для создания, редактирования и удаления нового поста
    """
    class Meta:
        model = Article
        fields = ('topic', 'article_body')
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-input'}),
            'article_body': SummernoteInplaceWidget(),  # при необходимости добавить стили виджета
        }                                               # https://github.com/summernote/django-summernote
