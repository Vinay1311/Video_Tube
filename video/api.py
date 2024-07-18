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
from video.serializers import PostVideoSerializer, GetVideoDetailsSerializer, GetVideoNUserDetailsSerializer, PostCommentSerializer, GetVideoCommentsSerializer,\
                                LikeVideoCommentPostSerializer
from video.models import VideoDetails, Playlist, Comment, Like


#---------------- Video Post Api ------------------- #
class PostVideoApi(generics.GenericAPIView):
    """
    APi to post the Video Details
    """

    serializer_class = PostVideoSerializer
    permission_classes = [IsAuthenticated]
    authenticate_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        data =  request.data.copy()
        video_id = self.request.GET.get(keys.VIDEO_ID, None)

        user = request.user.app_user
        data['users'] = user.id
        valid_formats = ['image/png', 'image/jpeg', 'image/jpg']

        video_file = data.get(keys.VIDEO_FILE, None)
        video_thumbnail = data.get(keys.VIDEO_THUMBNAIL, None)

        #Validation to Check Video_File & Video_Thumbnail is not null
        if video_thumbnail and video_file is None:
            return Response(ResponseHandling.failure_response_message(messages.INVALID_IMAGE_FORMAT, messages.OPERATION_FAILED), status=status400)
        
        if video_thumbnail is not None:
            data['flag_video_thumbnail'] = True

        #Checking the Video_thumbnail Format 
        # if video_thumbnail is not None and not video_thumbnail == '':
        #     if isinstance(video_thumbnail , str): 
        #         return Response(ResponseHandling.failure_response_message(messages.INVALID_IMAGE_FORMAT,messages.OPERATION_FAILED), status=status400)

        #     if video_thumbnail.content_type not in valid_formats:
        #         return Response(ResponseHandling.failure_response_message(messages.INVALID_IMAGE_FORMAT, messages.OPERATION_FAILED), status=status400)

            # data['video_thumbnail'] = video_thumbnail

        #pop the video_durtaion 
        # video_duration = data.pop('video_duration', None)
        # print("****", video_duration)

        if video_id is not None:
            video_instance = VideoDetails.objects.get(id = video_id)
            if video_instance:
                serializer = self.get_serializer(instance = video_instance, data = data)
                
            else:
                return Response(ResponseHandling.failure_response_message(messages.VIDEO_ID_NOT_EXISTS, messages.OPERATION_FAILED), status=status400)
        else:
            serializer = self.get_serializer(data = data)

        if not serializer.is_valid():
            errors = serializer.errors
            err =  error_message_function(errors)
            return Response(ResponseHandling.failure_response_message(err, messages.OPERATION_FAILED), status=status400)
        
        video = serializer.save()
        return Response(ResponseHandling.success_response_message(messages.VIDEO_DETAILS_SAVED, {keys.VIDEO_ID : video.id}), status=status200)
    

# #---------------- Upload Video Post Api ------------------- #
# class UploadVideoNThumbnailApi(generics.GenericAPIView):
#     """
#     APi to post the Video Details
#     """

#     serializer_class = UploadVideoThumbnailSerializer
#     permission_classes = [IsAuthenticated]
#     authenticate_classes = [JWTAuthentication]

#     def post(self, request, *args, **kwargs):
#         data =  request.data

#         #pop flag_video_thumbnail
#         flag_video_thumbnail = data.pop('flag_video_thumbnail')

#         serializer = self.get_serializer(data = data)
#         if not serializer.is_valid():
#             errors = serializer.errors
#             err =  error_message_function(errors)
#             return Response(ResponseHandling.failure_response_message(err, messages.OPERATION_FAILED), status=status400)
        
#         if flag_video_thumbnail:
#             thumbnail = serializer.save(flag_video_thumbnail = True)
#         else:
#             video = serializer.save(flag_video_thumbnail = False)

#         return Response(ResponseHandling.success_response_message(messages.FILE_UPLOADED_SUCCESSFULLY, serializer.data), status=status200)


#---------------- Video Details get Api ------------------- #
class GetVideoDetailsApi(generics.RetrieveAPIView):
    """ 
    Api to get Video Detail
    """

    serializer_class = GetVideoDetailsSerializer
    permission_classes = [IsAuthenticated]
    authenticate_classes = [JWTAuthentication]

    def retrieve(self, request, *args, **kwargs):
        video_id = self.request.GET.get(keys.VIDEO_ID, None)

        if video_id is None :
            return Response(ResponseHandling.failure_response_message(messages.THIS_FIELD_REQUIRED.format(keys.VIDEO_ID), ''),status=status400)
        
        queryset = VideoDetails.objects.get(id = video_id)
        serialzer = self.get_serializer(queryset)

        return Response(ResponseHandling.success_response_message(messages.VIDEO_DATA_FETCHED, serialzer.data), status=status200)
    
#---------------- Video Details List get Api ------------------- #
class GetVideoDetailsListApi(generics.ListAPIView):
    """ 
    Api to get Video Detail list
    """

    serializer_class = GetVideoDetailsSerializer
    permission_classes = [IsAuthenticated]
    authenticate_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        flag_user = self.request.GET.get(keys.FLAG_USER, None)

        if flag_user:
            #Retrieve User Video List
            user = request.user.app_user.id
            queryset = VideoDetails.objects.filter(users = user)

        else:
            #Retrieve all Video List
            queryset = VideoDetails.objects.all()

        serialzer = self.get_serializer(queryset, many =True)
        serialzer = GetVideoNUserDetailsSerializer(queryset, many =True)
        return Response(ResponseHandling.success_response_message(messages.VIDEO_DATA_FETCHED, serialzer.data), status=status200)

#---------------- Comment Post Api ------------------- #
class PostCommentApi(generics.GenericAPIView):
    """ 
    Api to Post Comment on Video
    """

    serializer_class = PostCommentSerializer
    permission_classes = [IsAuthenticated]
    authenticate_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        video_id = self.request.GET.get(keys.VIDEO_ID, None)
        comment_id = self.request.GET.get(keys.COMMENT_ID, None)

        if video_id is None:
            return Response(ResponseHandling.failure_response_message(messages.BAD_ITEM_REQUEST.format(keys.VIDEO_ID), ''), status= status400)

        #Commenting User 
        user = request.user.app_user.id 
        data['user'] = user

        #Video details
        video_instance = VideoDetails.objects.get(id = video_id)
        if video_instance:
            data['video'] = video_instance.id

        #Comment Save Section
        if comment_id is not None:
            comment_instance = Comment.objects.get(id = comment_id)
            data['flag_edited'] = True
            serializer = self.get_serializer(instance = comment_instance, data = data)
        else:
            serializer = self.get_serializer(data = data)

        if not serializer.is_valid():
            errors = serializer.errors
            err = error_message_function(errors)
            return Response(ResponseHandling.failure_response_message(errors, ''), status= status400)
        
        comment = serializer.save()
        return Response(ResponseHandling.success_response_message(messages.COMMENT_POSTED, {keys.COMMENT_ID: comment.id}), status=status200)
    
#---------------- Comment Post Api ------------------- #
class GetVideoCommentsApi(generics.ListAPIView):
    """ 
    Api to Get Comment List of a Video
    """

    serializer_class = GetVideoCommentsSerializer
    permission_classes = [IsAuthenticated]
    authenticate_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        video_id = self.request.GET.get(keys.VIDEO_ID, None)

        if video_id is None and video_id == '':
            return Response(ResponseHandling.failure_response_message(messages.BAD_ITEM_REQUEST.format(keys.VIDEO_ID), ''), status = status400)
        
        comments = Comment.objects.filter(video = video_id)
        serializer = self.get_serializer(comments, many = True, context={'request': request})

        return Response(ResponseHandling.success_response_message(messages.COMMENTS_FETCHED, serializer.data), status = status200)
    
#---------------- Comment Post Api ------------------- #
class LikeVideoCommentTwitterPostApi(generics.GenericAPIView):
    """ 
    Api Like Youtube Video, Comment Or Twittwer Post By User
    """

    serializer_class = LikeVideoCommentPostSerializer
    permission_classes = [IsAuthenticated]
    authenticate_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        video_id = data.pop(keys.VIDEO_ID, None)
        comment_id = data.pop(keys.COMMENT_ID, None)
        twitter_post_id = data.pop(keys.TWITTER_POST_ID, None)

        if video_id and comment_id and twitter_post_id is None:
             return Response(ResponseHandling.failure_response_message(messages.ID_REQUIRED, ''), status=status400)
        
        user = request.user.app_user.id
        data['user'] = user

        if video_id:
            video_instance = VideoDetails.objects.get(id = video_id)
            if video_instance is not None:
                video_instance.likes_count += 1
                video_instance.save()
                data['video'] = video_instance.id

                serializer = self.get_serializer(data = data)
            else:
                return Response(ResponseHandling.failure_response_message(messages.BAD_ITEM_REQUEST.format(keys.VIDEO_ID), ''), status=status400)
            
        if comment_id:
            comment_instance = Comment.objects.get(id = comment_id)
            if comment_instance is not None:
                comment_instance.like_counts += 1
                comment_instance.save()
                data['comment'] = comment_instance.id

                serializer = self.get_serializer(data = data)
            else:
                return Response(ResponseHandling.failure_response_message(messages.BAD_ITEM_REQUEST.format(keys.COMMENT_ID), ''), status=status400)
        # elif comment_id:
        #     serializer = self.get_serializer(user = user, comment = comment_id)

        # else:
        #     serializer = self.get_serializer(user = user, twitter_post = twitter_post_id)

        if not serializer.is_valid():
            errors = serializer.errors
            err = error_message_function(errors)
            return Response(ResponseHandling.failure_response_message(errors, ''), status= status400)

        like_instance = serializer.save()
        return Response(ResponseHandling.success_response_message(messages.OPERATION_SUCCESS, {keys.LIKE_ID: like_instance.id}), status = status200)
        