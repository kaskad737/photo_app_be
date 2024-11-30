from rest_framework import serializers
from .models import Photo, Frame


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ['id', 'photo', 'uploaded_by']


class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = ['id', 'frame', 'uploaded_by', 'restaurant']


class ListPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ['id', 'photo']


class RetrievePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = '__all__'
