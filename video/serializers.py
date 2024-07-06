#--------------- External Imports ----------------- #
from rest_framework import serializers

#--------------- Internal Imports ----------------- #
from helper import keys, messages
from video.models import VideoDetails


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