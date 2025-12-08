from django.contrib import admin
from .models import BlogEntry, BlogActivity

@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'image', 'created_at', 'user')
    search_fields = ('id', 'user')
    ordering = ['-created_at']

@admin.register(BlogActivity)
class BlogActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_entry', 'user', 'like', 'hide', 'comment', 'timestamp')
    search_fields = ('blog_entry__id', 'user__username', 'comment')
    ordering = ['-timestamp']
    

