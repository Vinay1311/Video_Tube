# ---------------- External Imports -----------------#
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
# ---------------- Internal Imports -----------------#
from helper import messages, keys
from helper.status import *
from helper.function import ResponseHandling, error_message_function
from twitter.serializers import PostTwitterPostSerializer, GetTwitterPostSerializer
from twitter.models import TwitterPost


#---------------- Twitter-Post Post Api ------------------- #
class PostTwitterPostsApi(generics.CreateAPIView):
    """ Post Api to Post the Twitter Post Of Users"""

    serializer_class = PostTwitterPostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        twitter_post_id = self.request.GET.get(keys.TWITTER_POST_ID, None)

        user = request.user.app_base
        data['user'] = user.id

        # Check Media Format
        valid_formats = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif','video/mp4']
        media_file = data.pop('media_file', None)
        if media_file is None and media_file == '':
            if isinstance(media_file , str): 
                return Response(ResponseHandling.failure_response_message(messages.INVALID_VIDEO_FORMAT,messages.OPERATION_FAILED), status=status400)

            if media_file.content_type not in valid_formats:
                return Response(ResponseHandling.failure_response_message(messages.INVALID_VIDEO_FORMAT, messages.OPERATION_FAILED), status=status400)

            data['media_file'] = media_file
            data['flag_media_file'] = True
        
        if twitter_post_id is not None and not twitter_post_id == '':
            twitter_post_instance = TwitterPost.objects.filter(id = twitter_post_id)
            if twitter_post_instance.exists():
                twitter_post_instance = twitter_post_instance.first()
                serializer = self.get_serializer(instance = twitter_post_instance, data = data)
            else:
                return Response(ResponseHandling.failure_response_message(messages.BAD_ITEM_REQUEST.format('twitter_post_id')),status = status400)
        
        serializer = self.get_serializer(data = data)

        if not serializer.is_valid():
            errors = serializer.errors
            err = error_message_function(errors)
            return Response(ResponseHandling.failure_response_message(errors, messages.OPERATION_FAILED), status400)
        
        twitter_post = serializer.save()
        return Response(ResponseHandling.success_response_message(messages.POSTED_SUCCESSFULLY, {keys.TWITTER_POST_ID: twitter_post.id}), status = status200)


#---------------- Twitter-Post Get Api ------------------- #
class GetTwitterPostsApi(generics.GenericAPIView):
    """ Get Api to Get the Twitter Post Of Users"""

    serializer_class = GetTwitterPostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        twitter_post_id = self.request.GET.get(keys.TWITTER_POST_ID, None)

        #Get User
        user = request.user.app_user.id

        # Getting Particular Post Of User
        if twitter_post_id is not None and not twitter_post_id == "":
            twitter_post_instance = TwitterPost.objects.get(id = twitter_post_id)
            serializer = self.get_serializer(instance = twitter_post_instance)
        
        # Getting 
        else:
            twitter_post_instance = TwitterPost.objects.filter(user = user).order_by('-created_by').order_by('-id')
            serializer = self.get_serializer(instance = twitter_post_instance, many = True)

        return Response(ResponseHandling.success_response_message(messages.DATA_FETCHED_SUCCESSFULLY, serializer.data), status=status200)


#----------------All Twitter-Post Get Api ------------------- #
class GetAllTwitterPostsApi(generics.ListAPIView):
    """ Get Api to Get All the Twitter Post Of All Users"""

    serializer_class = GetTwitterPostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):

        twitter_post_instance = TwitterPost.objects.all().order_by('-created_by').order_by('-id')
        serializer = self.get_serializer(instance = twitter_post_instance, many = True)

        return Response(ResponseHandling.success_response_message(messages.DATA_FETCHED_SUCCESSFULLY, serializer.data), status=status200)