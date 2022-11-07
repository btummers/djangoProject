from django.contrib import admin
from .models import Post

class postAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'text']
    search_fields = ['title', 'text']


admin.site.register(Post, postAdmin)

# Superuser:
# Brian
# Welkom01