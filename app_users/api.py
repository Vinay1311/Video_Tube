# ---------------- External Imports -----------------#
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
# ---------------- Internal Imports -----------------#
from helper import messages, keys
from helper.function import ResponseHandling, error_message_function, get_tokens_for_user
from helper.status import *
from app_users.models import UserDetails
from base_user.models import User
from app_users.serializers import PostUserDetailsSerializer, GetUserDetailsSerializer, UserLoginSerializer

# ---------------- Post User Register Api ---------------#
class PostUserRegisterApi(generics.CreateAPIView):
    """
    This is the Post api for save user details
    """
    serializer_class = PostUserDetailsSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        valid_format =['image/png', 'image/jpeg', 'image/jpg']

        #Create User with email
        user_email = data['email']
        user = User.objects.create(email = user_email)
        user.save()

        data['users'] = user.id

        #Check Valid Format of the Avatar & Cover Image
        avatar_image = request.FILES.get(keys.AVATAR_IMAGE, None)
        cover_image = request.FILES.get(keys.COVER_IMAGE, None)

        if avatar_image is not None and not avatar_image == "":
            if isinstance(avatar_image, str):
                return Response(ResponseHandling.failure_response_message(messages.INVALID_IMAGE_FORMAT, messages.OPERATION_FAILED), status= status400) 
            
            if avatar_image.content_type not in valid_format:
                return Response(ResponseHandling.failure_response_message(messages.INVALID_IMAGE_FORMAT, messages.OPERATION_FAILED), status= status400) 
            
        else:
            return Response(ResponseHandling.failure_response_message(messages.AVATAR_IMAGE_REQUIRED, messages.OPERATION_FAILED), status= status400) 
        
        if cover_image is not None:
            if isinstance(cover_image, str):
                return Response(ResponseHandling.failure_response_message(messages.INVALID_IMAGE_FORMAT, messages.OPERATION_FAILED), status= status400) 
            
            if cover_image.content_type not in valid_format:
                return Response(ResponseHandling.failure_response_message(messages.INVALID_IMAGE_FORMAT, messages.OPERATION_FAILED), status= status400) 
        
        #Hashing the Password
        password = data['password']
        data['password'] = make_password(password)

        serializer = self.get_serializer(data = data)
    
        if not serializer.is_valid():
            errors = serializer.errors
            err = error_message_function(errors)
            return Response(ResponseHandling.failure_response_message(err, ''), status= status400)
        
        serializer.save()
        return Response(ResponseHandling.success_response_message(messages.USER_DETAILS_SAVED, messages.OPERATION_SUCCESS), status=status200)
    
# ---------------- User Login post api ---------------- #
class PostUserLoginApi(generics.GenericAPIView):
    """
    Api for User Login
    """
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        email = data.get(keys.EMAIL)
        password = data.get(keys.PASSWORD)

        serializer = self.get_serializer(data = data)

        if not serializer.is_valid():
            errors = serializer.errors
            err = error_message_function(errors)
            return Response(ResponseHandling.failure_response_message(errors, ''), status= status400)

        user_instance = UserDetails.objects.filter(email = email).first()
        if user_instance:
            user_password = user_instance.password
            password = check_password(password, user_password)

            if password:
                user = user_instance
                if user is not None:
                    user_obj = User.objects.get(email = email)
                    token = get_tokens_for_user(user_obj)
                    return Response(ResponseHandling.success_response_message(messages.LOGIN_SUCCESSFULLY, token), status=status200)

            return Response(ResponseHandling.failure_response_message(messages.INCORRECT_PASSWORD, messages.OPERATION_FAILED), status=status400)
        return Response(ResponseHandling.failure_response_message(messages.INVALID_EMAIL, messages.OPERATION_FAILED), status=status400)

    
# ---------------- Get User Details Api ---------------- #
class GetUserDetailApi(generics.RetrieveAPIView):
    """
    This is the Get api to get user details
    """
    serializer_class = GetUserDetailsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def retrieve(self, request, *args, **kwargs):
        user_id = request.user.app_user.id

        user_instance = UserDetails.objects.get(id=user_id)
        serializer = self.get_serializer(instance = user_instance)
        return Response(ResponseHandling.success_response_message(messages.USER_DATA_FETCHED, serializer.data), status=status200)


# ---------------- Check Username Api ---------------#
class CheckUserName(generics.GenericAPIView):
    """
    This is the Get api to check username exists or not
    """
    def get(self, request, *args, **kwargs):
        username = request.GET.get(keys.USERNAME, None)

        if username is None and username == '':
            return Response(ResponseHandling.failure_response_message(messages.THIS_FIELD_REQUIRED.format(keys.USERNAME), ''), status=status400)
        
        # Checking Username is Existed or not
        username_instance = UserDetails.objects.filter(username__iexact = username).exists()
        if username_instance:
            return Response(ResponseHandling.success_response_message(messages.OPERATION_SUCCESS, {keys.IS_USERNAME_AVAILABLE: False}), status=status200)
        else:
            return Response(ResponseHandling.success_response_message(messages.OPERATION_SUCCESS, {keys.IS_USERNAME_AVAILABLE: True}), status=status200)