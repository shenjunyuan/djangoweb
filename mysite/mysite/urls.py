"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from trips.views import main, about, article, articleCreate, articleRead, articleUpdate, articleDelete, articleSearch, articleLike, commentCreate, commentUpdate, commentDelete
from account.views import register, login, logout


urlpatterns = [
    path('admin/', admin.site.urls),

    path('main/', view = main, name = 'main'),
    path('about/', view = about, name = 'about'),
    path('article/', view = article, name = 'article'),
    path('articleCreate/', view = articleCreate, name = 'articleCreate'),
    path('articleRead/<int:articleId>/', view = articleRead, name = 'articleRead'),
    path('articleUpdate/<int:articleId>/', view = articleUpdate, name = 'articleUpdate'),
    path('articleDelete/<int:articleId>/', view = articleDelete, name = 'articleDelete'),
    path('articleSearch/', view = articleSearch, name = 'articleSearch'),

    path('register/', view = register, name = 'register'),
    path('login/', view = login, name = 'login'),
    path('logout/', view = logout, name = 'logout'),

    path('articleLike/<int:articleId>/', view = articleLike, name = 'articleLike'),
    path('commentCreate/<int:articleId>/', view = commentCreate, name = 'commentCreate'),
    path('commentUpdate/<int:commentId>/', view = commentUpdate, name = 'commentUpdate'),
    path('commentDelete/<int:commentId>/', view = commentDelete, name = 'commentDelete'),

]
