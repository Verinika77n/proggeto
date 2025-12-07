from django.contrib import admin
from .models import BlogEntry

@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'image', 'created_at', 'user')
    search_fields = ('id', 'user')
    ordering = ['-created_at']

    

