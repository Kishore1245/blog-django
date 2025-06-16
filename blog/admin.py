from django.contrib import admin
from typing import Any
from .models import Post, Category, AboutUs

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at')

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(AboutUs)
 