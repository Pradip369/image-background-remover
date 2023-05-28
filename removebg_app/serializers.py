from rest_framework import serializers
from django.conf import settings
from bg_remover.global_const import constant

class FastBGRemoveSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

    def validate_image(self,img):
        if img.size > settings.MAX_FILE_SIZE:
            raise serializers.ValidationError("File must be less then or equal to 6MB")
        else:
            return img

class SlowBGRemoveSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    is_blur = serializers.BooleanField(default = False)
    is_grey = serializers.BooleanField(default = False)
    detect = serializers.ChoiceField(choices = constant.DETECT_CHOICES,default = 'person')
    blur_type = serializers.ChoiceField(choices = constant.BLUR_TYPE,default = 'moderate')

    def validate_image(self,img):
        if img.size > settings.MAX_FILE_SIZE:
            raise serializers.ValidationError("File must be less then or equal to 6MB")
        else:
            return img