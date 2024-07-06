from django.contrib import admin
from video.models import *

@admin.register(VideoDetails)
class VideoDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','users','video_title','likes_count','comments_count']
    search_fields = ['users','video_title']
    search_fields = ['flag_is_published']
    readonly_fields = ['created', 'modified']

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['id','users','playlist_name','number_of_videos']
    search_fields = ['users','playlist_name']
    readonly_fields = ['created', 'modified']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','video','user','content','flag_edited']
    search_fields = ['user','video']
    search_fields = ['flag_edited']
    readonly_fields = ['created', 'modified']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','user','video','comment']
    search_fields = ['user','video','comment']
    search_fields = ['flag_like']
    readonly_fields = ['created', 'modified']
