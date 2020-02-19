from django.db import models
from account.models import User
# 修改model.py後，執行 python manage.py makemigrations 產生 SQL 程式
# 再執行 python manage.py migrate 建立資料表

class Article(models.Model):
    title = models.CharField(max_length=128, unique=True)   # unique=True : 內文不重複
    content = models.TextField()
    pubDateTime = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-pubDateTime'] # 文章時間倒排


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # 表示「連串刪除」，亦即當所指的外來資料刪除時，本資料一併刪除。
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
    pubDateTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.article.title + '-' + str(self.id)
    class Meta:
        ordering = ['pubDateTime'] # 留言時間正排

