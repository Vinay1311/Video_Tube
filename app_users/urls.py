from django.urls import path
from app_users.api import *

urlpatterns = [

#Get 
path('get-userdetails/', GetUserDetailApi.as_view()), #URL to get the user Details
path('check-username/', CheckUserName.as_view()), #URL to check username is unique or not

#Post
path('user-register/', PostUserRegisterApi.as_view()), #URL to register User
path('user-login/', PostUserLoginApi.as_view()), #URL to login User

]