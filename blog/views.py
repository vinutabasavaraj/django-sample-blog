from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from datetime import date
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect,Http404
from django.views.generic import ListView, DetailView
from django.views import View
from django.urls import reverse


from .models import Post
from .forms import CommentForm


class StartingPage(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"
    
    
    def get_queryset(self):
        query_set = super().get_queryset()[:3]
        return query_set
    

# Create your views here.
# def stating_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request,"blog/index.html", {
#         "posts" : latest_posts
#     })

class AllPosts(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"
    
# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request,"blog/all-posts.html", {
#         "all_posts" : all_posts
#     })


class SinglePost(View):
    # template_name = "blog/post-detail.html"
    # model = Post
    
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
            
        return is_saved_for_later
        
        
    
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            "post" : post,
            "post_tags" : post.tag.all(),
            "comment_form" : CommentForm(),
            "comments" : post.comments.all().order_by("-id"),
            "saved_for_later" : self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context )
        
        
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("posts-detais-page"), args=[slug])
        
        
        context = {
            "post" : post,
            "post_tags" : post.tag.all(),
            "comment_form" : comment_form,
            "comments" : post.comments.all().order_by("-id"),
            "saved_for_later" : self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context )    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tag.all()
        context["comment_form"] = CommentForm()
        return context
    

# def post_details(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     #Post.objects.get(slug=slug)
#     return render(request,"blog/post-detail.html", {
#         "post" : identified_post,
#         "post_tags" : identified_post.tag.all()
#     })
    
class ReadLaterView(View):
    
    def get(self, request):
        stored_post = request.session.get("stored_posts")
        
        context = {}
        if stored_post is None or len(stored_post)==0:
            context["post"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_post)
            context["post"] = posts
            context["has_posts"] = True
            
        return render(request, "blog/stored_post.html", context)
    
    def post(self, request):
        stored_post = request.session.get("stored_posts")
        if stored_post is None:
            stored_post = []
        
        post_id = int(request.POST["post_id"])
        
        if post_id not in stored_post:
            stored_post.append(post_id)
            request.session["stored_posts"] = stored_post
        else:
            stored_post.remove(post_id)
        request.session["stored_posts"] = stored_post
            
        return HttpResponseRedirect("/")
            