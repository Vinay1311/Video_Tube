from django.contrib import admin
from twitter.models import *

@admin.register(TwitterPost)
class TwitterPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'media_file']
    search_fields = ['id', 'user']
    list_filter = ['flag_media_file']
    readonly_fields = ['created', 'modified']
    

