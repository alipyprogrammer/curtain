from django.urls import path, include, re_path
from .views import *
from . import views
from rest_framework import routers
from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    # Detail
    re_path(
        r'my-card/',
        views.my_card, name="my_card"
    ),
    re_path(
        r'pre-invoice/',
        views.pre_invoice, name="my_card"
    ),

    re_path(
        r'my-factor/',
        views.my_factor, name="my_card"
    ),




    re_path(
        r'add-to-card/',
        views.add_to_card, name="add_to_card"
    ),
    re_path(
        r'update-to-card/',
        views.update_to_card, name="update_to_card"
    ),
    re_path(
        r'remove-to-card/(?P<pk>[-\w]+)/',
        views.remove_to_card, name="ProductDetail"
    ),
    path('bankgateways/', az_bank_gateways_urls()),
    path('go-to-geteway/', go_to_gateway_view),
    path('callback-gateway/', callback_gateway_view),
]

