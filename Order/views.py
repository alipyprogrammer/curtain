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

from User.models import Address
from .serializer import *
from rest_framework import status, filters
from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from core.pagination import PaginationConfig
from .serializer import *
from .models import *
import json
from rest_framework.parsers import JSONParser

import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from django.db.models import Subquery, OuterRef, Sum, F
from django.db.models.functions import Coalesce
from Functions.sms import *
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def my_card(request):
    user = request.user
    orm_get =  Card.objects.filter(user=user)
    serializer = CardListSerializer(orm_get, many=True)
    dic = {}
    if orm_get.exists():
        df_sum = pd.DataFrame(serializer.data)
        sum_product = df_sum['property'].sum()
        dic = {
            "data": serializer.data,
            "count": len(serializer.data),
            "sum" : sum_product,
            "message": "success"
        }
    else:
        dic ={
            "data": [],
            "message": "not found"
        }
    return Response(dic,status=status.HTTP_200_OK)


@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def update_to_card(request):
    data = JSONParser().parse(request)
    serializer = CardSerializer(data=data, many=False)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def add_to_card(request):
    data = JSONParser().parse(request)
    serializer = CardSerializer(data=data, many=False)
    if serializer.is_valid():
        # Check if the record exists
        filter_exist = Card.objects.filter(
            user=request.user,
            product=serializer.validated_data['product'],
            property=serializer.validated_data['property']
        ).first()  # Get the first matching record, if any

        if filter_exist:
            # Update the existing record
            serializer = CardSerializer(filter_exist, data=data, many=False)
            if serializer.is_valid():
                serializer.save(user=request.user)
                filter_exist = Card.objects.filter(
                    user=request.user,
                )
                data_response = serializer.data
                data_response['count'] = len(filter_exist)
                return Response(data_response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Create a new record if it does not exist
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def remove_to_card(request,pk):
    get =  get_object_or_404(Card,id=pk, user=request.user).delete()
    return Response("done", status=200)



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def pre_invoice(request):

    ################
    # ORM
    my_card  = Card.objects.filter(user= request.user)
    exists_2fa  = my_card.filter(product__lte=100).exists()
    my_card  = CardFullSerializer(my_card, many=True)
    get_address = Address.objects.get(id=request.data['address'])
    # ORM
    ################
    get_gold_price = Gold.objects.last().value


    factor = Factor.objects.create(
    user_id      =  request.user.id,
        name=request.data['name'],
        address      =  get_address.address,
        post_code    =  get_address.address,
        city         = get_address.city,
        mobile       = request.user.mobile,
        pay_status   = False,
        has_2fa      = exists_2fa,
        status_code  = 4,
        type_ads     = request.data['type_ads']
    )
    for i in my_card.data:
        property_create = PropertyItem.objects.create(
            accessory_id = i["property"]["accessory"]["id"],
            accessory_name = i["property"]["accessory"]["name"],
            accessory_price = i["property"]["accessory"]["price"],
            plating = i["property"]["plating"],
            help_price = i["property"]["help_price"],
            size = i["property"]["size"],
            weight = i["property"]["weight"],
            count_in_stock = i["property"]["count_in_stock"],
            salary = i["property"]["salary"],
        )
        factor_item = FactorItem.objects.create(
            product_id          = i["product"]["_id"],
            count               = i["count"],
            pre_cost_percent    = i["product"]["pre_cost_percent"],
            date_available      = i["product"]["date_available"],
            gold_price          = get_gold_price,
            create_date         = timezone.now()
        )
        factor_item.property.add(property_create)
        factor_item.save()
        factor.item.add(factor_item)
        factor.save()
    return Response({
        "status": 200,
        "message": "success",
        "success": True,
        "data" : {
            "id": factor.id
        }
    }, status=status.HTTP_200_OK)



@api_view(["POST"])
def my_factor(request):
    #flag start
    ################
    flag =  True
    df_data_get = None
    ################
    #flag end

    try:
        id_value = request.data['id']
        flag     = True
    except:
        flag     = False
    product =  None
    if flag:
        get      = Factor.objects.filter(id=request.data['id'])
        data_get = get.values_list("item",flat=True)
        get_item = FactorItem.objects.filter(
            id__in=data_get
        ).values(
            "property__help_price", "update_date", "product",
            "product__name", "product__image", "property__salary","property__weight","property__size",
            "property__accessory_name", "property__accessory_price" , "property__plating",
            "property__salary", "pre_cost_percent"
        )
        df_data_get = pd.DataFrame(get_item)
        df_data_get = df_data_get.sort_values(by=['update_date'])
        df_data_get = df_data_get.drop_duplicates(subset=['product'],keep='last')
        if get.first().status_code == 1 :
            product  = json.loads(df_data_get.to_json(orient='records'))
        df_data_get = float(df_data_get['property__help_price'].sum())
    else:
        get = Factor.objects.filter(user=request.user)
    data = FactorSerializer(get, many=True).data

    return Response({
        "data":data,
        "product" : product,
        "status":200,
        "message":"success",
        "sum" : df_data_get,
        "status_factor" : get.first().status_code,
        "success":True,
    }, status=status.HTTP_200_OK)




@api_view(["GET"])
def go_to_gateway_view(request):

    factor = Factor.objects.get(id=request.GET.get('id'))
    latest_property_subquery = PropertyItem.objects.filter(
        factoritem__id=OuterRef('id')
    ).order_by('-create_date').values('help_price')[:1]
    total_help_price = FactorItem.objects.filter(
        factor__id=factor.id
    ).annotate(
        latest_help_price=Subquery(latest_property_subquery)
    ).aggregate(
        total=Coalesce(Sum('latest_help_price'), 0)
    )




    amount = total_help_price['total']
    user_mobile_number = factor.user.mobile

    factory = bankfactories.BankFactory()
    try:
        bank = factory.create()
        bank.set_request(request)
        bank.set_amount(amount)
        bank.set_client_callback_url('/api/order/callback-gateway/')
        bank.set_mobile_number(user_mobile_number)

        bank_record = bank.ready()
        #to_do Create validate_factor_object

        create_vldt = ValidateFactor.objects.create(
            factor = factor,
            tracking_id = bank_record.tracking_code
        )

        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e




def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    if bank_record.is_success:

        get_vldt = ValidateFactor.objects.filter(tracking_id=bank_record.tracking_code)

        if get_vldt.exists():
            pre_cost_ls = get_vldt.values_list('factor__item__pre_cost_percent', flat=True)
            ls_filter = list(filter(lambda x: True if x < 100 else False, pre_cost_ls))
            
            factor_get = get_vldt.first().factor
            mobile_get = factor_get.user.mobile
            if len(ls_filter) != 0:
                factor_get.status_code = 2  # waiting for build
                factor_get.save()
                message =  "با تشکر از خرید شما" + "\n" + "سفارش شما ثبت شد و در حال ساخت می باشد به محض ساخته شدن سفارش کارشناسان ما با شما تماس خواهند گرفت"
                send_sms_2(
                    [mobile_get],
                    [message]
                )
            else:
                factor_get.status_code = 1  # order_accepted
                factor_get.save()
                message = "با تشکر از خرید شما" + "\n"+ "سفارش شماثبت شد و در اسرع وقت به دستتان خواهد رسید"
                send_sms_2(
                    [mobile_get],
                    [message]
                )
        else:
            message = "خطا پرداختا" + "\n" + "رکورد پرداخت شده بانک در دیتا بیس یافت نشد"++ "\n" +f"{tracking_code}"
            send_sms_2(
                ['09197718346', '09011488075'],
                [message]
            )
        return HttpResponse(f"پرداخت با موفقیت انجام شد  {bank_record}.")

    return HttpResponse(
        f"پرداخت با شکست مواجه شده است.{bank_record} اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")
