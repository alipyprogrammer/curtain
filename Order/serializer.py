from rest_framework import serializers
from .models import *
import pandas as pd
from scrape.models import Gold
from django.core.cache import cache
from django.db.models import F, Max, Min
from Product.serializer import *

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        exclude = ['user']



class CardFullSerializer(serializers.ModelSerializer):
    property = serializers.SerializerMethodField(read_only=True)
    product = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Card
        exclude = ['user']

    @staticmethod
    def get_product(obj):
        product    = obj.product
        product    =  ProductSerializer(product).data
        del product['properties']
        return product
    @staticmethod
    def get_property(obj):
        get_property    = obj.property
        get_property    =  PropertiesSerializer(get_property).data
        return get_property



class PropertyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyItem
        fields = '__all__'

class CardListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    property = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Card
        exclude = ['user']

    @staticmethod
    def get_product(obj):
        product    = obj.product
        product    =  ProductSerializer(product).data
        del product['properties']
        return product

    @staticmethod
    def get_property(obj):
        property    = obj.property.help_price
        return property




class FactorItemSerializer(serializers.ModelSerializer):
    property = PropertyItemSerializer(many=True)
    product = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = FactorItem
        fields = '__all__'
    @staticmethod
    def get_product(obj):
        product    = obj.product.name
        return product

class FactorSerializer(serializers.ModelSerializer):
    item = FactorItemSerializer(many=True)

    class Meta:
        model = Factor
        fields = '__all__'
