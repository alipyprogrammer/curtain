# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.decorators import  api_view,permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView ,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import *
from .serializer import *

from rest_framework import status

from datetime import datetime

from rest_framework.viewsets import ModelViewSet

from User.permissions import *



#LIST
class MainCategoriesList(ListAPIView):
    queryset =MainCategories.objects.all()
    serializer_class =MainCategoriesSerializer

class SubcategoriesList(ListAPIView):
    queryset =Subcategories.objects.all()
    serializer_class =SubcategoriesSerializer


class BlogList(ListAPIView):
    queryset =Blog.objects.all()
    serializer_class =BlogSerializer
    filterset_fields = ('main_category__slug' , 'sub_category__slug')




#DETAIL
class MainCategoriesDetail(RetrieveAPIView):
    queryset =MainCategories.objects.all()
    serializer_class =MainCategoriesSerializer
    lookup_field ="slug"


class SubcategoriesDetail(RetrieveAPIView):
    queryset =Subcategories.objects.all()
    serializer_class =SubcategoriesSerializer
    lookup_field ="slug"


class BlogDetail(RetrieveAPIView):
    queryset =Blog.objects.all()
    serializer_class =BlogSerializer
    lookup_field ="slug"




