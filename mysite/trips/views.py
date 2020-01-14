from django.shortcuts import render, reverse
from datetime import datetime
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import Post
from .form import PostForm


def home(request):
    query = request.GET.get('q')

    if query:
        post_list = Post.objects.filter(Q(title__contains=query) | Q(content__contains=query))
    else:
        post_list = Post.objects.all()

    return render(request, 'home.html', {'post_list': post_list })


class PostCreate(CreateView):
    form_class = PostForm
    template_name = "create_post.html"
    success_url = reverse_lazy('home')

class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwag ='pk'
    template_name = 'create_post.html'

    def get_success_url(self):
        id = self.get_object().id
        return reverse('post_detail', kwargs={'pk': id})


class PostDelete(DeleteView):
    model = Post
    pk_url_kwag ='pk'
    success_url = reverse_lazy('home')

class PostDetail(DetailView):
    model = Post
    pk_url_kwag ='pk'
    template_name = 'post.html'



