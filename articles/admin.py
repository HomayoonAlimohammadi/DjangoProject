from django.contrib import admin

from articles.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content','slug', 'timestamp', 'updated']
    search_fields = ['title', 'content', 'id']
    raw_id_fields = ['user']

admin.site.register(Article, ArticleAdmin)