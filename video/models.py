# ---------------- External Imports -----------------#
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import now
from django.core.validators import RegexValidator

# ---------------- Internal Imports -----------------#
from helper.models import CreationModeificationBase
from app_users.models import UserDetails

class VideoDetails(CreationModeificationBase):
    """Model to store the video details"""
    users = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="user_video_details")
    video_file = models.FileField(null=True, blank=True, upload_to="media/files/video_file/videos/")
    video_thumbnail = models.ImageField(null=True, blank=True, upload_to="media/files/video_file/videos_thumbanail/")
    flag_video_thumbnail = models.BooleanField(default=False)
    video_title = models.CharField(max_length=250, null=True, blank=True)
    video_description = models.TextField(null=True, blank=True)
    video_duration = models.CharField(max_length=20, null=True, blank=True)
    flag_is_published = models.BooleanField(default= False)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    def __str__(self) :
        return f'{self.id}'

class Playlist(CreationModeificationBase):
    """Model to store the playlist details"""
    users = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="user_playlist")
    videos = models.ManyToManyField(VideoDetails, related_name='playlist_videos')
    playlist_name = models.CharField(max_length=250, null=True, blank=True)
    playlist_description = models.TextField(null=True, blank=True)
    playlist_thumbnail = models.ImageField(null=True, blank=True, upload_to="media/files/video_file/playlist_thumbanail/")
    number_of_videos = models.IntegerField(default=0)

    def __str__(self) :
        return self.playlist_name
    
class Comment(CreationModeificationBase):
    """Model to store the like details"""
    user = models.OneToOneField(UserDetails, on_delete=models.CASCADE, related_name="commented_by_user")
    video = models.ForeignKey(VideoDetails, on_delete=models.CASCADE, related_name="comments_on_video")
    content = models.TextField(null=True, blank=True)
    flag_edited = models.BooleanField(default=False)

    def __str__(self) :
        return f'{self.id}-{self.user}'
    

class Like(CreationModeificationBase):
    """Model to store the like details"""
    user = models.OneToOneField(UserDetails, on_delete=models.CASCADE, related_name="liked_by_user")
    video = models.OneToOneField(VideoDetails, on_delete=models.CASCADE, related_name="like_video")
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name="like_comments")
    # twitter = models.OneToOneField(Twitter, on_delete=models.CASCADE, related_name="like_twittwer_post")
    flag_like = models.BooleanField(default=False)

    def __str__(self) :
        return f'{self.video}-{self.user}'