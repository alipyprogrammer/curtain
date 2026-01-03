from itertools import product
from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ( 
    get_object_or_404,
    CreateAPIView,
    ListCreateAPIView,
    ListAPIView,

    RetrieveAPIView,
    DestroyAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status, filters
from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from core.pagination import PaginationConfig
from .serializers import (
     MainCategoriesSerializer
    ,SubcategoriesSerializer
    ,ProductListNSerializer
    ,ProductSerializer
)
from .models import *
import json
from django.core.cache import cache
from django.db import transaction
from django.db.models import Max, Min, Count

#listBlock

def main_category(request, slug):

    dict_send = {}

    get_main_category_detail = get_object_or_404(
        Subcategories,
        slug=slug
    )
    dict_send['detail'] = MainCategoriesSerializer(
        get_main_category_detail
    ).data



    get_sub_category_list = get_object_or_404(
        Subcategories,
        main__slug=slug
    )

    dict_send['list_category'] = SubcategoriesSerializer(
        get_sub_category_list, many=True
    ).data





    return Response(dict_send)

@api_view(['GET'])
def product_detail(request, slug, main_category, sub_category):
    get_header = get_object_or_404(
        Product,
        slug=slug,
        main_category__slug=main_category,
        sub_category__slug=sub_category,
        draft=False
    )
    serializer_class = ProductSerializer(get_header)


    return Response(serializer_class.data)


class ProductFilter(APIView):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        number_disp_prod_start = int(page - 1) * 10
        number_disp_prod_end = int(page) * 10
        query_price = request.GET.dict()
        del query_price['page']
        query = {k: v for k, v in query_price.items() if v and v!="undefined"}
        query['draft'] = False


        product_count = Product.objects.filter(**query).count()
        product_page = product_count // 10
        queryset = Product.objects.filter(**query).order_by('-create_at')[number_disp_prod_start:number_disp_prod_end]
        serialized_data = ProductSerializer(queryset, many=True)


        if not queryset.exists():
            return Response(
                data={"mssg":"Not_Found_Any_Record"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            data={"product":serialized_data.data, "page":product_page},
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def product_category_list(request, main_category, sub_category=None):
    dic_send = {}


    if not sub_category:
        get_category = get_object_or_404(MainCategories, slug=main_category)
        dic_send['category_detail'] = MainCategoriesSerializer(get_category).data
    else:
        get_sub_category = get_object_or_404(
            Subcategories, slug=sub_category, main__slug=main_category
        )
        get_category = get_object_or_404(MainCategories, slug=main_category)

        dic_send['category_detail'] = SubcategoriesSerializer(get_sub_category, many=False).data
        dic_send['main_category'] = MainCategoriesSerializer(get_category, many=False).data
    
    page = int(request.GET.get('page', 1))
    number_disp_prod_start = (page - 1) * 10
    number_disp_prod_end = page * 10
    
    query = request.GET.dict()
    query.pop('page', None)
    query = {k: v for k, v in query.items() if v and v != "undefined"}
    
    product_filter = {
        'main_category__slug': main_category,
        'draft': False
    }
    if sub_category:
        product_filter['sub_category__slug'] = sub_category
    
    get_product = Product.objects.filter(**product_filter).filter(**query)
    
    product_count = get_product.count()
    product_page = product_count // 10
    get_product = get_product.order_by('-create_at')[number_disp_prod_start:number_disp_prod_end]
    
    dic_send["setting"] = {
        'page': product_page,
        'event': EventType.objects.all().values("id", "name")
    }
    
    dic_send['product'] = ProductListNSerializer(get_product, many=True).data
    dic_send['event_list'] = EventType.objects.all().values("id", "name")


    get_sub_category = Subcategories.objects.filter(
        main__slug=main_category
    )

    dic_send['sub_categories'] = SubcategoriesSerializer(
        get_sub_category, many=True
    ).data



    return Response(dic_send)



@api_view(['POST'])
def installment_price_calculator(request):
    prod_id = request.data.get('prod_id')
    product_get = Product.objects.get(id = prod_id )
    period = product_get.properties.installment_period_month
    precost = product_get.properties.pre_cost_percent
    finall_price = request.data.get('final_price')
    month_pay = ( finall_price - (finall_price * precost) ) / period
    return Response(status = 200,data = {'month_pay':month_pay})

#(price - (price * 20%)) /  3 month (period)