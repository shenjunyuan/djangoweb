from django.contrib import admin
from .models import Post # 新增post這個table讓admin帳號有權限使用
# Register your models here.

admin.site.register(Post)