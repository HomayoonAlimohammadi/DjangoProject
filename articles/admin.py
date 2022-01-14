from django.contrib import admin

from articles.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content']
    search_fields = ['title', 'content', 'id']

admin.site.register(Article, ArticleAdmin)