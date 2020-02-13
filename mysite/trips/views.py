from datetime import datetime
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.urls.base import reverse_lazy, reverse
from django.db.models.query_utils import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



from .models import Article, Comment
from .form import ArticleForm
from account.models import User

def admin_required(func):
    def auth(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, '請以管理者身份登入')
            return redirect(reverse('login') + '?next=' + request.get_full_path())
        return func(request, *args, **kwargs)
    return auth


def main(request):
    context = {'like':'Django 很棒'}
    return render(request, 'main.html', context)

def about(request):
    return render(request, 'about.html')

def article(request):
    # 將 articles 變數改為一個字典 (Dictionary)，其中每個項目的鍵 (Key) 就是文章物件，而其對應值 (Value) 就是所屬的留言查詢集 (Queryset)
    articles = {article:Comment.objects.filter(article=article) for article in Article.objects.all()} # 在每篇文章下方顯示所屬留言
    context = {'articles': articles}
    return render(request, 'article.html', context)

@login_required
def articleCreate(request):
    template = 'articleCreateUpdate.html'

    if request.method == 'GET':
        return render(request, template, {'articleForm':ArticleForm()})

    # POST
    articleForm = ArticleForm(request.POST) # request.POST 是使用者在表單裡所填的資料，透過 HTML 表單送到後端
    if not articleForm.is_valid():
        return render(request, template, {'articleForm':articleForm})

    articleForm.save()
    messages.success(request, '文章已新增')
    return redirect('article')


def articleRead(request, articleId):
    '''
    Read an article
        1. Get the article instance; redirect to the 404 page if not found
        2. Render the articleRead template with the article instance and its
           associated comments
    '''
    article = get_object_or_404(Article, id=articleId)
    context = {
        'article': article,
        'comments': Comment.objects.filter(article=article)
    }
    return render(request, 'articleRead.html', context)

@login_required
def articleUpdate(request, articleId):
    '''
    Update the article instance:
        1. Get the article to update; redirect to 404 if not found
        2. If method is GET, render a bound form
        3. If method is POST,
           * validate the form and render a bound form if the form is invalid
           * else, save it to the model and redirect to the articleRead page
    '''
    article = get_object_or_404(Article, id=articleId)
    template = 'articleCreateUpdate.html'
    if request.method == 'GET':
        articleForm = ArticleForm(instance=article)
        return render(request, template, {'articleForm':articleForm})

    # POST
    articleForm = ArticleForm(request.POST, instance=article)
    if not articleForm.is_valid():
        return render(request, template, {'articleForm':articleForm})

    articleForm.save()
    messages.success(request, '文章已修改')
    return redirect('articleRead', articleId=articleId)

@admin_required
def articleDelete(request, articleId):
    '''
    Delete the article instance:
        1. Render the article page if the method is GET
        2. Get the article to delete; redirect to 404 if not found
    '''
    if request.method == 'GET':
        return redirect('article')

    # POST
    article = get_object_or_404(Article, id=articleId)
    article.delete()
    messages.success(request, '文章已刪除')
    return redirect('article')

def articleSearch(request):
    '''
    Search for articles:
        1. Get the "searchTerm" from the HTML form
        2. Use "searchTerm" for filtering
    '''
    searchTerm = request.GET.get('searchTerm')
    articles = Article.objects.filter( Q(title__icontains=searchTerm) | Q(content__icontains=searchTerm) )
    context = {'articles':articles, 'searchTerm':searchTerm}
    return render(request, 'articleSearch.html', context)
@login_required
def articleLike(request, articleId):
    '''
    Add the user to the 'likes' field:
        1. Get the article; redirect to 404 if not found
        2. If the user does not exist in the "likes" field, add him/her
        3. Finally, call articleRead() function to render the article
    '''
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
