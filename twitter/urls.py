from django.urls import path
from twitter.api import *

urlpatterns = [

#Get
path('get-tweet/', GetTwitterPostsApi.as_view()), #URL to get user all or specific post api
path('get-all-tweet/', GetAllTwitterPostsApi.as_view()), #URL to get all users all posts 

#Post
path('post-tweet/', PostTwitterPostsApi.as_view()), #URL to Post twitter post 
]