from django.contrib import admin

from .models import Post, Comment, Food, Provider

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Food)
admin.site.register(Provider)
