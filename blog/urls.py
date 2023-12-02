from django.urls import path
from . import views


urlpatterns = [
    path("", views.StartingPage.as_view(), name="stating-page"),#It triggers /challange/
    path("posts", views.AllPosts.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePost.as_view(), name = "posts-detais-page"),
    path("read-later", views.ReadLaterView.as_view(), name = "read-later")
]
