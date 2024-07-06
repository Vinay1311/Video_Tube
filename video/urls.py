from django.urls import path
from video.api import *

urlpatterns = [

#Get
path('get-video-data/', GetVideoDetailsApi.as_view()), #Url to Get Video Details

#Post
path('video-data/', PostVideoApi.as_view()), #Url to Post video data
# path('upload-video-contents/', UploadVideoNThumbnailApi.as_view()), #Url to Upload video content, video or thumbnail
]