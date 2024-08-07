#--------------- External Imports ----------------- #
from rest_framework import serializers

#--------------- Internal Imports ----------------- #
from app_users.models import UserDetails
from video.models import VideoDetails
from helper import messages, keys

#----------------- Post User Details Serializer -----------------
class PostUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['users', 'fullname', 'username', 'email','avatar_image','cover_image','password']
        required_fields = ['fullname', 'username', 'email','avatar_image','cover_image','password']
        def validate(self, data):
            for field_name in self.required_fields:
              # Check if the field is present in the validated data and if it's empty
                if field_name not in data or not data[field_name]:
                   
                    raise serializers.ValidationError({messages.THIS_FIELD_REQUIRED.format(field_name)})

#----------------- Post User login Serializer -----------------               
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['email' , 'password']
        required_fields = ['email', 'password']

        def validate(self, data):
            for field_name in self.required_fields:
              # Check if the field is present in the validated data and if it's empty
                if field_name not in data or not data[field_name]:
                   
                    raise serializers.ValidationError({messages.THIS_FIELD_REQUIRED.format(field_name)})

                
#----------------- Get User Details Serializer -----------------
class GetUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id','users', 'fullname', 'username', 'email','avatar_image','cover_image']

#----------------- Get User Watched Video History Details Serializer -----------------
class GetUserWatchedVideoHistorySerializer(serializers.ModelSerializer):
    videos_history = serializers.SerializerMethodField()
    class Meta:
        model = UserDetails
        fields = ['videos_history']

    def get_videos_history(self, instance):
        video_instances = VideoDetails.objects.filter(id = instance.videos_history.id)
        return VideoDetailsSerializer(video_instances, many=True).data
    

#----------------- Get Video Details Serializer -----------------
class VideoDetailsSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    class Meta:
        model = VideoDetails
        fields = ['id','video_title','video_thumbnail','video_duration','user_details']

    def get_user_details(self, instance):
        user_instance = UserDetails.objects.filter(id = instance.users.id).first()
        if user_instance:
            serializer = GetUserDetailsSerializer(user_instance, context=self.context)
            return serializer.data
        return {}
    