from django.db import models
# 修改model.py後，執行 python manage.py makemigrations 更新資料庫
# 再執行 python manage.py migrate 將欄位寫入資料庫

class Post(models.Model): # 宣告一個 Post 類別， 定義欄位屬性
    title = models.CharField('標題',max_length = 100) # max_length=100 -- 標題不可以超過 100 個字元
    content = models.TextField('內容',blank = True) # blank=True -- 非必填欄位（表單驗證時使用），預設所有欄位都是 blank=False
    photo = models.URLField('照片網址',blank = True)
    location = models.CharField('地點',max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True) # auto_now_add=True -- 物件新增的時間。若想設成物件修改時間，則用 auto_now=True

    def __str__(self): # 讓標題能顯示出來
        return self.title


