from django.contrib import admin

from app.models import Comment, Post, Subscribe, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Subscribe)
