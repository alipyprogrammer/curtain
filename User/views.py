from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
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
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers
from django.core.cache import cache
from django.contrib.auth import authenticate
import requests
import json
import json
from rest_framework.parsers import JSONParser
from Functions.token import create_token
from Functions.token import *
from Functions.sms import send_sms_2
from django.utils import timezone
from django.contrib.auth.hashers import make_password



class MyTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=username, password=password)
        data = {}
        data['krabo'] = {}
        if not user:
            data['krabo']["status"] = 400
        else:
            refresh = RefreshToken.for_user(user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            user_serializer = UserSerializerWithToken(user)
            user_data = user_serializer.data
            for k, v in user_data.items():
                data['krabo'][k] = v
            data['krabo']["status"] = 200
        return data

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)

        # Add custom claims
        token['username'] = user.username
        token[
            'message'] = 'سلام به سایت کرابو خوش آمدید (ساخته شده توسط علی عبادی و ارمان پرواز) -> کرابو خونمون قبل اینکه کاشی همه چیو خراب کنه'

        return token


@api_view(['post'])
def my_token_obtain_pair(request):
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
                serializer = MyTokenObtainPairSerializer(data=request.data)
            else:
                ttl = cache.ttl(Data['token'])
                cache.delete(Data['token_sms'])
                cache.set(Data['token_sms'], get_cache, timeout=ttl)
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

    try:
        serializer.is_valid(raise_exception=True)
    except TokenError as e:
        raise InvalidToken(e.args[0])

    data_response = serializer.validated_data
    if data_response['krabo']['status'] == 200:
        data_response['krabo']['refresh'] = data_response['refresh']
        data_response['krabo']['token'] = data_response['access']
        del data_response["refresh"]
        del data_response["access"]
        return Response(
            data_response, status=status.HTTP_200_OK
        )

    else:
        return Response(serializer.validated_data, status=403)



@api_view(['post'])
@ip_lockdown([],1)
def register_user_send_code(request):
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
            else:
                ttl = cache.ttl(Data['token'])
                cache.delete(Data['token'])
                cache.set(Data['token'], get_cache, timeout=ttl)
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

    orm_exists = User.objects.filter(mobile=Data['mobile'])
    if orm_exists.exists():
        return Response({"user exists"},status=422)

    list_number = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    number = int(
        ''.join(str(random.choice(list_number)) for _ in range(4))
    )

    token = create_token("register")
    cache.set(token, {
        "mobile": Data['mobile'],
        "password" : Data['password'],
        "type_ads" : Data['type_ads'],
        "number": number,
        "date"  : [datetime.now()]
    }, timeout=6000)
    message = f"کد ورود :  {number} \n لغو 11"
    send_sms_2(
        [Data['mobile']],
        [message]
    )

    return Response({
        "status": 200,
        "success": True,
        "message": "done",
        "data" :token
    }, status=200)



@api_view(["POST","PUT"])
def code_sms(request):
    Data = request.data
    get_cache = cache.get(Data['token_sms'])
    if None == get_cache:
        return Response({
            "status": 404,
            "success": False,
            "message": "token not found "
        }, status=404)


    if request.method == "POST":
        if int(Data['number']) == int(get_cache['number']) :
            now = datetime.now()
            time_difference = now - get_cache["date"][-1]

            if time_difference.total_seconds() / 60 > 12:
                return Response({
                    "status": 429,
                    "success": True,
                    "data": None,
                    "message": "کد شما منقصی شده است"
                }, status=429)


            else:
                hashed_password = make_password(get_cache['password'])

                add_user = User.objects.create(
                    username   = get_cache['mobile'],
                    mobile     = get_cache['mobile'],
                    type_ads   = get_cache['type_ads'],
                    password   = hashed_password,
                    is_active  = True
                )

                serializer = MyTokenObtainPairSerializer(
                    data={
                        "username":get_cache['mobile'],
                        "password": get_cache['password'],

                    })

                try:
                    serializer.is_valid(raise_exception=True)
                except TokenError as e:
                    raise InvalidToken(e.args[0])
                data_response = serializer.validated_data
                if data_response['krabo']['status'] == 200:
                    data_response['krabo']['refresh'] = data_response['refresh']
                    data_response['krabo']['token'] = data_response['access']
                    del data_response["refresh"]
                    del data_response["access"]

                return Response({
                    "status": data_response['krabo']['status'],
                    # "success": True,
                    "data": data_response,
                    "message": "success"
                }, status=data_response['krabo']['status'])



        else:
            return Response({
                "status": 403,
                "success": True,
                "data": None,
                "message": "number not found"
            }, status=403)
    if request.method == "PUT":
        now = datetime.now()
        time_difference = now - get_cache["date"][-1]
        if time_difference.total_seconds() / 60 > 3:

            list_number = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            number = int(
                ''.join(str(random.choice(list_number)) for _ in range(4))
            )

            get_cache['date'].append(
                datetime.now()
            )
            get_cache['number'] = number
            ttl = cache.ttl(Data['token_sms'])
            cache.delete(Data['token_sms'])
            cache.set(Data['token_sms'], get_cache, timeout=ttl)
            message = f"کد ورود :  {number} \n لغو 11"
            send_sms_2(
                [get_cache['mobile']],
                [message]
            )
            return Response({
                "status": 200,
                "success": True,
                "message": "done",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": 429,
                "success": True,
                "data": None,
                "message": "شما یه کد معتبر دارید"
            }, status=429)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsManager,)
    ordering = '-id'


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes = (IsManager,)


@api_view(['PUT'])
@permission_classes([IsManager])
def UpdatePasswordUser(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    data = request.data
    user.username = data['username']
    user.phoneNumber = data['phoneNumber']
    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)


# class UserAdd(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserUpdate(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsManager,)


class UserDelete(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsManager,)

@api_view(['POST', 'PUT', 'GET', 'DELETE'])
def my_address(request):

    if request.method == 'GET':
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        address_id = data.get('id') 
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return Response({"status": 404, "message": "not found"}, status=404)
        
        serializer = AddressSerializer(address, data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        address_id = request.data.get('id') 
        get = Address.objects.filter(user=request.user, id=address_id)
        if get.exists():
            get.delete()
            return Response({"status": 200, "message": "ok"}, status=200)
        return Response({"status": 404, "message": "not found"}, status=404)


@api_view(['POST', 'PUT', 'GET'])
def my_profile(request):
    if request.method == 'GET':
        addresses = Address.objects.filter(user=request.user)
        address_serializer = AddressSerializer(addresses, many=True).data
        get =  User.objects.filter(id=request.user.id)
        user_serializer = UserProfileSerializer(get).data
        data_response = {}
        data_response['user']    = user_serializer
        data_response['address'] = address_serializer
        return Response(data_response,status=200)
