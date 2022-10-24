from django import forms
from django.core.exceptions import ValidationError

from .models import Article, Category
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

class ArticleCategoryForm(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.all(),
        initial=0
    )

    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(ArticleCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Название категории'

    # def clean_name(self):
    #     data = self.cleaned_data['name']
    #     if data == None:
    #         raise ValidationError("Выберите хотя бы одну категорию..")


