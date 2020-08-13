from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from . models import Post

class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "my_blog/home.html"

    def get_queryset(self):
        return Post.objects.order_by('-date_posted')
    
class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = "post"

class PostCreateView(LoginRequiredMixin,generic.edit.CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,generic.edit.UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return self.get_object().author == self.request.user

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,generic.DetailView):
    model = Post
    success_url = "/"
    template_name_suffix = "_delete"
    context_object_name = "post"

    def test_func(self):
        return self.get_object().author == self.request.user

def about(request):
    return render(request,'my_blog/about.html',{'title': "About"})
