from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from . models import Post

class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "my_blog/home.html"
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "my_blog/user_posts.html"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')
    
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

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,generic.edit.DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')
    template_name = "my_blog/post_delete.html"
    context_object_name = "post"

    def test_func(self):
        return self.get_object().author == self.request.user

def about(request):
    return render(request,'my_blog/about.html',{'title': "About"})
