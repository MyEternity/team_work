from django import forms
from .models import Article, Comment, Category
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ArticleAddUpdateDeleteForm(forms.ModelForm):
    topic = forms.CharField(widget=forms.TextInput())
    article_body = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Article
        fields = ('topic', 'article_body')

    def __init__(self, *args, **kwargs):
        super(ArticleAddUpdateDeleteForm, self).__init__(*args, **kwargs)
        self.fields['topic'].widget.attrs['placeholder'] = 'Введите название статьи'
        self.fields['topic'].label = 'Название статьи'
        self.fields['topic'].width = '90%'
        self.fields['article_body'].label = 'Текст статьи'


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = 'Сообщение'


class SelectCategoryForm(forms.ModelForm):
    name = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=Category.choices)

    def __init__(self, *args, **kwargs):
        super(SelectCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Название категории'

    class Meta:
        model = Category
        fields = ('name',)
