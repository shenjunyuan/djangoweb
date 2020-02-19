from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    title = forms.CharField(label='標題', max_length=128)
    content = forms.CharField(label='內容', widget=forms.Textarea) # Widget 為表單小工具，用來設定頁面中的輸入模式 ， 此處為 Textarea

    class Meta:
        model = Article # 檢查欄位跟model的table是否一致
        fields = ['title', 'content', 'user']
        widgets = {'user': forms.HiddenInput()}



