#--------------- External Imports ----------------- #
from rest_framework import serializers

#--------------- Internal Imports ----------------- #
from helper import keys, messages
from video.models import VideoDetails, Comment, Like
from app_users.models import UserDetails


# -------------------- Post Video Serializer -------------------- #
class PostVideoSerializer(serializers.ModelSerializer):
    """Post Video Serializer to post the vidoe details"""
    class Meta:
        model = VideoDetails
        fields = ['users','video_title','video_file','video_thumbnail','video_description','video_duration']
        required_fields = ['video_title','video_file','video_thumbnail','video_description','video_duration']

        def validate(self, data):
            for field_name in self.required_fields:
              # Check if the field is present in the validated data and if it's empty
                if field_name not in data or not data[field_name]:
                   
                    raise serializers.ValidationError({messages.THIS_FIELD_REQUIRED.format(field_name)})

# # -------------------- Post Video Serializer -------------------- #
# class UploadVideoThumbnailSerializer(serializers.ModelSerializer):
#     """Upload Video_Thumbnail_Serializer to upload the video & thumbnail of the video"""

#     class Meta:
#         model = VideoDetails
#         fields = ['id','video_file','video_thumbnail']

# -------------------- Get Video Details Serializer -------------------- #
class GetVideoDetailsSerializer(serializers.ModelSerializer):
    """Get Video Details Serializer to get the video details"""
    class Meta:
        model = VideoDetails
        fields = ['id','users','video_title','video_file','video_thumbnail','video_description','video_duration','flag_is_published','likes_count','comments_count']

# -------------------- Get Video Details Serializer -------------------- #
class GetVideoNUserDetailsSerializer(serializers.ModelSerializer):
    """Get Video & User Details Serializer to get the video details along with user details"""
    user_details = serializers.SerializerMethodField()
    class Meta:
        model = VideoDetails
        fields = ['id','users','video_title','video_file','video_thumbnail','video_description','video_duration','flag_is_published','likes_count','comments_count', 'user_details']

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
        fields = ['id','users','fullname','avatar_image']

# -------------------- Post Comment Details Serializer -------------------- #
class PostCommentSerializer(serializers.ModelSerializer):
    """Post Comment Serializer to Post the comment on video"""

    flag_edited =  serializers.SerializerMethodField()
    edited_tag =  serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['user','video','content','flag_edited', 'edited_tag']

    def get_flag_edited(self, instance):
        return instance.flag_edited

    def get_edited_tag(self, instance):
        print("123->",instance.flag_edited)
        if instance.flag_edited == True:
            instance.content = f'{instance.content} (edited)'
            instance.save()
        return instance.content

     
# -------------------- Get Comment Details Serializer -------------------- #
class GetVideoCommentsSerializer(serializers.ModelSerializer):
    """Get Video-Comment Serializer to Get all comments of a video"""
    comment_id =  serializers.SerializerMethodField()
    user_details =  serializers.SerializerMethodField()
    # flag_edited =  serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['comment_id','user_details','content','flag_edited','like_counts']

    def get_comment_id(self, instance):
        return instance.id

    def get_user_details(self, instance):
        user_instance = UserDetails.objects.filter(id = instance.user.id).first()
        if user_instance:
            serializer = GetUserDetailsSerializer(user_instance, context=self.context)
            return serializer.data
        return {}
    
    # def get_flag_edited(self, instance):
    #     if instance.flag_edited == True:
    #         instance.content = f'{instance.content} (edited)'
    #         instance.save()

    
# -------------------- Get User Details Serializer -------------------- #
class GetUserDetailsSerializer(serializers.ModelSerializer):
    """Get User-Detail Serializer to Get User Details"""
    avatar_image = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()
    class Meta:
        model = UserDetails
        fields = ['id','fullname','username','email','avatar_image','cover_image']

    def get_avatar_image(self, instance):
        avatar_image = instance.avatar_image
        if avatar_image:
            request = self.context.get('request')
            if request:
                avatar_image_url = request.build_absolute_uri(avatar_image.url)
                return avatar_image_url
        return ''
    
    def get_cover_image(self, instance):
        if instance.cover_image:
            request = self.context.get('request')
            if request:
                cover_image_url = request.build_absolute_uri(instance.cover_image.url)
                return cover_image_url
        return ''
    
    
# -------------------- Get User Details Serializer -------------------- #
class LikeVideoCommentPostSerializer(serializers.ModelSerializer):
    """ Serializer to Like video, comment & twitter post """

    class Meta:
        model = Like
        fields = ['user','video','comment']