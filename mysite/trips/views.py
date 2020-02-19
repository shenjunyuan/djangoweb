from datetime import datetime
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.urls.base import reverse_lazy, reverse
from django.db.models.query_utils import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


from .models import Article, Comment
from .form import ArticleForm
from account.models import User

def main(request):
    latest_content = Article.objects.all()
    if latest_content:
        latest_content = Article.objects.all().order_by('-id')[0]
    else:
        latest_content = '無最新消息'
    context = {'welcome':'歡迎光臨', 'latest_content':latest_content }
    return render(request, 'main.html', context)

def about(request):
    return render(request, 'about.html')

def article(request):
    articles = { article:Comment.objects.filter( article = article ) for article in Article.objects.all() } # 抓取每篇文章底下留言資料
    context = {'articles': articles}
    return render(request, 'article.html', context )

@login_required
def articleCreate(request):
    template = 'articleCreateUpdate.html'

    if request.method == 'GET':
        return render(request, template, {'articleForm':ArticleForm(), 'request': request})
    # POST
    # Reference type
    # instance type
    data = request.POST.copy() # request.POST 是使用者在html表單裡所填的資料，送到後端
    data.update({'user': request.user.id})
    articleForm = ArticleForm(data)

    if not articleForm.is_valid(): # 驗證輸入的資料格式是否正確
        return render(request, template, {'articleForm':articleForm})

    articleForm.save()
    messages.success(request, '文章已新增')
    return redirect('article')


def articleRead(request, articleId): # articleId 是從 URL request 傳來

    article = get_object_or_404(Article, id=articleId)
    context = {
        'article': article,
        'comments': Comment.objects.filter(article=article)
    }
    return render(request, 'articleRead.html', context)

@login_required
def articleUpdate(request, articleId):

    article = get_object_or_404(Article, id=articleId)
    template = 'articleCreateUpdate.html'
    if request.method == 'GET':
        articleForm = ArticleForm(instance=article) # 產生一個 Django 表單並綁定從資料庫取出的物件
        return render(request, template, {'articleForm':articleForm})

    articleForm = ArticleForm(request.POST, instance=article) # 產生一個 Django 表單而且綁定兩個項目：使用者的輸入以及所取出的文章物件

    if not articleForm.is_valid():
        return render(request, template, {'articleForm':articleForm})

    articleForm.save()
    messages.success(request, '文章已修改')
    return redirect('articleRead', articleId=articleId)

@login_required
def articleDelete(request, articleId):
    article = get_object_or_404(Article, id=articleId)
    if request.method == 'GET':
       return HttpResponseForbidden()
    elif article.user == request.user or request.user.is_superuser:
        article.delete()
        messages.success(request, '文章已刪除')
        return redirect('article')
    else:
        return HttpResponseForbidden()

def articleSearch(request):
    search = request.GET.get('search')
    articles = Article.objects.filter( Q(title__icontains=search) | Q(content__icontains=search) )
    context = {'articles':articles, 'search':search}
    return render(request, 'articleSearch.html', context)

@login_required
def articleLike(request, articleId):
    article = get_object_or_404(Article, id=articleId)
    if request.user not in article.likes.all():
        article.likes.add(request.user)
    return articleRead(request, articleId)

@login_required
def commentCreate(request, articleId):
    '''
    Create a comment for an article:
        1. Get the "comment" from the HTML form
        2. Store it to database
    '''
    if request.method == 'GET':
        return articleRead(request, articleId)

    # POST
    comment = request.POST.get('comment')
    if comment:
        comment = comment.strip()
    if not comment:
        return redirect('articleRead', articleId=articleId)

    article = get_object_or_404(Article, id=articleId)
    Comment.objects.create(article=article, user=request.user, content=comment)
    return redirect('articleRead', articleId=articleId)

@login_required
def commentUpdate(request, commentId):
    '''
    Update a comment:
        1. Get the comment to update and its article; redirect to 404 if not found
        2. If it is a 'GET' request, return
        3. If the comment's author is not the user, return
        4. If comment is empty, delete the comment, else update the comment
    '''
    commentToUpdate = get_object_or_404(Comment, id=commentId)
    article = get_object_or_404(Article, id=commentToUpdate.article.id)
    if request.method == 'GET':
        return articleRead(request, article.id)

    # POST
    if commentToUpdate.user != request.user:
        messages.error(request, '無修改權限')
        return redirect('articleRead', articleId=article.id)

    comment = request.POST.get('comment', '').strip()
    if not comment:
        commentToUpdate.delete()
    else:
        commentToUpdate.content = comment
        commentToUpdate.save()
    return redirect('articleRead', articleId=article.id)

@login_required
def commentDelete(request, commentId):
    '''
    Delete a comment:
        1. Get the comment to update and its article; redirect to 404 if not found
        2. If it is a 'GET' request, return
        3. If the comment's author is not the user, return
        4. Delete the comment
    '''
    comment = get_object_or_404(Comment, id=commentId)
    article = get_object_or_404(Article, id=comment.article.id)
    if request.method == 'GET':
        return articleRead(request, article.id)

    # POST
    if comment.user != request.user:
        messages.error(request, '無刪除權限')
        return redirect('articleRead', articleId=article.id)

    comment.delete()
    return redirect('articleRead', articleId=article.id)


