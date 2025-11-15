from rest_framework import serializers
from .models import *


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = '__all__'
