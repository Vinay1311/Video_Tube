# ---------------- External Imports -----------------#
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import now
from django.core.validators import RegexValidator

# ---------------- Internal Imports -----------------#
from helper.models import CreationModeificationBase
from helper import regex_validator
from helper import messages
from base_user.models import User

class UserDetails(CreationModeificationBase):
    """ User Details of the App """
    users = models.OneToOneField(User, on_delete=models.CASCADE , related_name='app_user')
    fullname = models.CharField(max_length=350)
    username = models.CharField(max_length=150)
    email = models.EmailField(validators=[regex_validator.email_regex])
    avatar_image = models.ImageField(null=True, blank= True, upload_to='media/files/user_avatar_images/')
    cover_image = models.ImageField(null=True, blank= True, upload_to='media/files/user_cover_images/')
    password = models.CharField(max_length=200)
    videos_history = models.ForeignKey('video.VideoDetails', on_delete=models.CASCADE, null=True, blank=True, related_name='user_video_history')

    def __str__(self):
        return str(self.fullname)