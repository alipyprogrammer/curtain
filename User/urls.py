from django.urls import path, include, re_path
from . import views
from .views import *

from . import views_captcha
from .views_captcha import *

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [

    path('add-log-user/', views.add_log_user, name='add_log_user'),
    path('generate-captcha/', views_captcha.generate_captcha, name='generate-captcha'),
    path('check-captcha/', views_captcha.check_captcha, name='generate-captcha'),
    path('login', views.my_token_obtain_pair, name='token_obtain_pair'),

    path('profile/', views.getUserProfile, name="UserProfile"),
    path('list/', UserList.as_view(), name='UserList'),
    # path('expert/list/' , ExpertList.as_view() , name='ExpertList'),
    # path('presenter/list/' , PresenterList.as_view() , name='PresenterList'),

    path('update/<str:pk>/', UserUpdate.as_view(), name="UserUpdate"),
    path('delete/<str:pk>/', UserDelete.as_view(), name="UserUpdate"),
    # path('add/', UserAdd.as_view(), name="UserAdd"),
    path(
        'register/',
        views.register_user_send_code,
        name="user_register"
    ),
    path(
        'code-sms/',
        views.code_sms,
        name="user_register"
    ),


    # path('add/factor/' ,views.UserAddInFactor ,name="UserAddInFactor"),

    re_path(r'detail/(?P<id>[-\w]+)', UserDetail.as_view(), name="ImageBlogDetailPanelAdmin"),


    re_path('my-address/', views.my_address),
    re_path('profile/', views.my_profile),



]

