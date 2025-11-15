from itertools import product
from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ( 
    CreateAPIView,
    ListCreateAPIView ,
    ListAPIView,
    get_object_or_404,

    RetrieveAPIView,
    DestroyAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializer import *
from rest_framework import status, filters
from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from Product.serializer import ProductListNSerializer
class SliderList(ListAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    filterset_fields = (
        'status',
    )
class BannerList(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    filterset_fields = (
        'status',
    )



@api_view(['GET'])
def header(request, pk):
    get_header = get_object_or_404(NavBar, idd=pk)
    get_header_serilizers = NavBarSerializer(get_header)

    return Response({
            "status": True,
            "message": "done",
            "data": get_header_serilizers.data
        }, status=200)

@api_view(['GET'])
def home(request, pk):
    dic_send = {}
    get_home_obj = get_object_or_404(Home, idd=pk, status=True)
    get_header_serilizers = NavBarSerializer(get_home_obj.header)

    get_slider_serilizers = SliderSerializer(get_home_obj.slider.filter(status=True), many=True)
    get_banner_serilizers = BannerSerializer(get_home_obj.banner.filter(status=True), many=True)
    get_suggestion_box_serilizers = BoxSerializer(get_home_obj.box, many=True)


    dic_send['header'] = get_header_serilizers.data
    dic_send['slider'] = get_slider_serilizers.data
    dic_send['banner'] = get_banner_serilizers.data

    #suggestion_box
    ##############
    dic_send['box'] = get_suggestion_box_serilizers.data
    # if not list(dic_send['suggestion_box']['category_id']) == []:
    #     get_product = Product.objects.filter(
    #         main_category__in=list(dic_send['suggestion_box']['category_id']),
    #         new=dic_send['suggestion_box']['new'],
    #         suggested=dic_send['suggestion_box']['suggested'],
    #         draft=False
    #     ).order_by("-_id")[:dic_send['suggestion_box']['count']]
    #
    #
    # get_products_serilizers = ProductListNSerializer(get_product, many=True)
    # dic_send['suggestion_box']['products'] = get_products_serilizers.data
    # del dic_send['suggestion_box']['category_id']



    #suggestion_box
    ####################


    return Response({
            "status": True,
            "message": "done",
            "data": dic_send
        }, status=200)


