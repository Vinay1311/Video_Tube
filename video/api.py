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
from video.serializers import PostVideoSerializer, GetVideoDetailsSerializer
from video.models import VideoDetails, Playlist, Comment, Like


#---------------- Video Post Api ------------------- #
class PostVideoApi(generics.CreateAPIView):
    """
    APi to post the Video Details
    """

    permission_classes = [IsAuthenticated]
    authenticate_classes = [JWTAuthentication]
    serializer_class = PostVideoSerializer

    def create(self, request, *args, **kwargs):
        data =  request.data
        video_id = self.request.GET.get(keys.VIDEO_ID, None)

        user = request.user.app_user.id
        data['users'] = user
        valid_formats = ['image/png', 'image/jpeg', 'image/jpg']

        video_file = data.get(keys.VIDEO_FILE, None)
        video_thumbnail = data.get(keys.VIDEO_THUMBNAIL, None)

        #Validation to Check Video_File & Video_Thumbnail is not null
        if video_thumbnail and video_file is None:
            return Response(ResponseHandling.failure_response_message(messages.INVALID_IMAGE_FORMAT, messages.OPERATION_FAILED), status=status400)

        #Checking the Video_thumbnail Format 
        # if video_thumbnail is not None and not video_thumbnail == '':
        #     if isinstance(video_thumbnail , str): 
        #         return Response(ResponseHandling.failure_response_message(messages.INVALID_IMAGE_FORMAT,messages.OPERATION_FAILED), status=status400)

        #     if video_thumbnail.content_type not in valid_formats:
        #         return Response(ResponseHandling.failure_response_message(messages.INVALID_IMAGE_FORMAT, messages.OPERATION_FAILED), status=status400)

            # data['video_thumbnail'] = video_thumbnail

        if video_id is not None:
            video_instance = VideoDetails.objects.filter(id = video_id)
            if video_instance.exists():
                serializer = self.get_serializer(instance = video_instance, data = data, partial=True)
            else:
                return Response(ResponseHandling.failure_response_message(messages.VIDEO_ID_NOT_EXISTS, messages.OPERATION_FAILED), status=status400)

        serializer = self.get_serializer(data = data, partial = True)

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

    serializer_class = PostVideoSerializer
    permission_classes = [IsAuthenticated]
    authenticate_classes = [JWTAuthentication]

    def retrieve(self, request, *args, **kwargs):
        video_id = request.GET.get(keys.VIDEO_ID, None)

        if video_id is None :
            return Response(ResponseHandling.failure_response_message(messages.THIS_FIELD_REQUIRED.format(keys.VIDEO_ID), ''),status=status400)
        
        queryset = VideoDetails.objects.get(id = video_id)
        serialzer = self.get_serializer(queryset)

        return Response(ResponseHandling.success_response_message(messages.VIDEO_DATA_FETCHED, serialzer.data), status=status200)