from django.urls import path
from video.api import *

urlpatterns = [

#Get
path('get-video-data/', GetVideoDetailsApi.as_view()), #Url to Get Video Details
path('get-video-data-list/', GetVideoDetailsListApi.as_view()), #Url to Get Video Details for User or all list
path('get-video-comments-list/', GetVideoCommentsApi.as_view()), #Url to Get Comments of a Video

#Post
path('video-data/', PostVideoApi.as_view()), #Url to Post video data
path('comment-data/', PostCommentApi.as_view()), #Url to Post Comment Data
path('like-content/', LikeVideoCommentTwitterPostApi.as_view()), #Url to Like Video , Comment or Twitter Post of User
# path('upload-video-contents/', UploadVideoNThumbnailApi.as_view()), #Url to Upload video content, video or thumbnail
]