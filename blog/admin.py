from django.contrib import admin

from .models import Post, Author, Tag, Comment


class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tag", "date")
    list_display =("title", "author", "date")
    prepopulated_fields = {"slug" : ("title",)}
    
class CommentAdminClass(admin.ModelAdmin):
    list_display =("user_name", "post")
    

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdminClass)
