# ---------------- External Imports -----------------#
from django.db import models

# ---------------- Internal Imports -----------------#
from helper.models import CreationModeificationBase
from app_users.models import UserDetails

class TwitterPost(CreationModeificationBase):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='twitter_posts')
    content = models.TextField()
    media_file = models.FileField(null=True, blank=True, upload_to='media/files/twitter_files/')
    flag_media_file = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.user.fullname}'