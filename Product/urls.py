from django.urls import path, include, re_path
from .views import *
from . import views
from rest_framework import routers
from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    path('installment_price_calculator/', installment_price_calculator),
]
