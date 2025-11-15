from django.urls import path, include, re_path
from .views import *
from . import views
from rest_framework import routers

urlpatterns = [

    path("slider/", SliderList.as_view(), name="productList"),
    path("banner", BannerList.as_view(), name="productList"),


    re_path(r'header/(?P<pk>[-\w]+)/', views.header, name="ProductDetail"),
    re_path(r'home/(?P<pk>[-\w]+)/', views.home, name="home"),





]