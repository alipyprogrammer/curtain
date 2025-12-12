from rest_framework import serializers
from .models import *
from Img.serializer import ImgSerializer


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class BoxSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Box
        fields = "__all__"

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
