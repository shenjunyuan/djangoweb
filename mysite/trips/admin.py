from django.contrib import admin
from .models import Article, Comment
# Register your models here.
# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/


class CommentAdmin(admin.ModelAdmin): # 增加一個 CommentAdmin 類別 (繼承 admin.ModelAdmin)
    list_display = ['article', 'content', 'pubDateTime'] # 客製化頁面顯示清單 (list_diaplay)：顯示 article 與 content 欄位
    list_display_links = ['article'] # 設定資料連結欄位 (list_diaplay_links)：透過 article 來連結 (此項為預設)
    list_filter = ['article', 'content'] # 設定右方過濾欄位為 article 與 content，點選即可濾出該項目的相關資料
    search_fields = ['content'] # 設定 content 為搜尋欄位
    list_editable = ['content'] # 設定 content 欄位可編輯

    class Meta:
        model = Comment

admin.site.register(Article)
admin.site.register(Comment, CommentAdmin)