from rest_framework import serializers
from .models import *
import pandas as pd
from Img.serializer import ImgSerializer
from Product.serializer import *
import random


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'



class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class BoxSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    product = serializers.SerializerMethodField(read_only=True)
    img = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Box
        fields = "__all__"

    @staticmethod
    def get_category(obj):
        category_data = list(obj.category.values("id", "name"))
        if category_data:
            dic_all = [{"id": 0, "name": "همه"}]
            category_data = dic_all + category_data
        return category_data
    @staticmethod
    def get_product(obj):
        category = obj.category.values_list("id", flat=True)
        if category:
            products_by_category = []

            for cat in category:
                products = Product.objects.filter(
                    main_category=cat,
                    new=obj.new,
                    suggested=obj.suggested,
                    draft=False
                ).order_by("-_id")[:10]
                products_by_category.extend(products)

            category = ProductListNSerializer(products_by_category, many=True).data
            random.shuffle(category)
        return category

    @staticmethod
    def get_img(obj):
        img = obj.img
        serializer = ImgSerializer(img, many=True).data
        return serializer



# Header Start
###########################
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuItemTitleSerializer(serializers.ModelSerializer):
    item  = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MenuItemTitle
        fields = '__all__'
    @staticmethod
    def get_item(obj):
        list_order = ['index']
        item = obj.item.order_by(*list_order)
        serializer = MenuItemSerializer(item, many=True)
        return serializer.data

class MenuSerializer(serializers.ModelSerializer):
    menu_item  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'

    @staticmethod
    def get_menu_item(obj):
        menu_item = obj.menu_item
        serializer = MenuItemTitleSerializer(menu_item, many=True)
        return serializer.data

class NavBarSerializer(serializers.ModelSerializer):
    menu  = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = NavBar
        fields = '__all__'

    @staticmethod
    def get_menu(obj):
        menu = obj.menu
        serializer = MenuSerializer(menu, many=True)
        return serializer.data

# Header End
###########################
