from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from Functions.sms import token
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView
from django.contrib.auth.hashers import make_password
from rest_framework import status
# from User import get_user_model
from django.contrib.auth import get_user_model
from .permissions import *
from .filter import *
from django.contrib.auth.hashers import make_password
import cv2
import numpy as np
import random
from .models import *
from django.core.cache import cache
import hashlib
from datetime import datetime
from Functions.views import list_to_sha512
from Functions.token import create_token
import base64
from time import sleep


@api_view(['GET'])
def generate_captcha(request):
    Data = request.data

    token = create_token("captcha")

    number_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    text = ''.join(str(random.choice(number_list)) for _ in range(4))

    cache.set(token, {
        "token": token,
        "code": text,
        # "ip"    : "192.168.23.10",
        "try": 0
    }, timeout=70)

    image = np.ones((500, 500, 3), dtype=np.uint8) * 200
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 5
    font_color = (0, 0, 0)
    thickness = 5

    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    position = (image.shape[1] // 2 - text_width // 2, image.shape[0] // 2 + text_height // 2)
    cv2.putText(image, text, position, font, font_scale, font_color, thickness)

    list_number = [0, 1, 2, 3, 4, 5]
    color_list = [(0, 0, 0), (255, 0, 0), (0, 4, 255), (32, 255, 0), (255, 84, 0), (0, 255, 183)]
    num_lines = 30
    for _ in range(num_lines):
        start_point = (np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0]))
        end_point = (np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0]))
        number = random.choice(list_number)

        line_color = color_list[number]
        line_thickness = 5
        cv2.line(image, start_point, end_point, line_color, line_thickness)

    encoded_image = cv2.imencode('.jpg', image)[1]
    image_buffer = encoded_image.tobytes()
    image_base64 = base64.b64encode(image_buffer).decode('utf-8')
    return Response({
        "status": 200,
        "success": True,
        "data": {
            "token": token,
            "image": image_base64
        }
    }, status=200)


@api_view(['POST'])
def check_captcha(request):
    Data = request.data
    get_cache = cache.get(Data['token'])
    if get_cache == None:
        return Response({
            "status": 404,
            "success": False,
            "message": " token not found "
        }, status=404)
    else:
        if get_cache['try'] < 4:
            get_cache['try'] = get_cache['try'] + 1
            if str(get_cache['code']) == str(Data['code']):
                cache.delete(Data['token'])
                return Response({
                    "status": 200,
                    "success": True,
                }, status=200)
            else:
                cache.set(Data['token'], get_cache)
                return Response({
                    "status": 403,
                    "success": True,
                    "message": "code not found"
                }, status=403)
        else:
            cache.delete(Data['token'])
            return Response({
                "status": 403,
                "success": True,
                "message": "You tried too hard!"
            }, status=403)







