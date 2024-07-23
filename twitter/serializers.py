#--------------- External Imports ----------------- #
from rest_framework import serializers

#--------------- Internal Imports ----------------- #
from helper import keys, messages
from twitter.models import TwitterPost
from app_users.models import UserDetails

# ----------------- Post Twitter-Posts Serializer ----------------- #
class PostTwitterPostSerializer(serializers.ModelSerializer):
    """ Serializer for Post Twitter Post of Users"""
    class Meta:
        model = TwitterPost
        fields = ['user','content','media_file','flag_media_file']

# ----------------- Post Twitter-Posts Serializer ----------------- #
class GetTwitterPostSerializer(serializers.ModelSerializer):
    """ Serializer for Get Twitter Post of Users"""
    user_details = serializers.SerializerMethodField()
    class Meta:
        model = TwitterPost
        fields = ['id','user_details','content','media_file','flag_media_file']

    def get_user_details(self, instance):
        user_instance = UserDetails.objects.filter(id = instance.users.id).first()
        if user_instance:
            serializer = GetUserDetailsSerializer(user_instance)
            return serializer.data
        return {}
    

# -------------------- Get User Details Serializer -------------------- #
class GetUserDetailsSerializer(serializers.ModelSerializer):
    """Get User Details Serializer to get the user details"""
    class Meta:
        model = UserDetails
        fields = ['id','users','fullname','username','avatar_image']