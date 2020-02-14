from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    title = forms.CharField(label='標題', max_length=128)
    content = forms.CharField(label='內容', widget=forms.Textarea)

    class Meta:
        model = Article
        fields = ['title', 'content', 'user']
        widgets = {'user': forms.HiddenInput()}

