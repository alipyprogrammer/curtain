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
    items = serializers.SerializerMethodField()

    class Meta:
        model = Box
        fields = "__all__"

    @staticmethod
    def get_img(obj):
        img = obj.img
        serializer = ImgSerializer(img, many=True).data
        return serializer

    def get_items(self, obj):
        if not obj.content_type:
            return []

        model = obj.content_type.model_class()
        if not model:
            return []

        qs = model.objects.all()

        settings = obj.content_type_setting or {}

        # filter
        filters = settings.get("filter")
        if filters:
            qs = qs.filter(**filters)

        # exclude
        excludes = settings.get("exclude")
        if excludes:
            qs = qs.exclude(**excludes)

        # order_by
        order_by = settings.get("order_by")
        if order_by:
            qs = qs.order_by(*order_by)

        # limit
        limit = settings.get("limit")
        if limit:
            qs = qs[:limit]

        serializer_class = self.get_dynamic_serializer(model)
        return serializer_class(qs, many=True, context=self.context).data

    def get_dynamic_serializer(self, model):
        from django.core.exceptions import ImproperlyConfigured

        serializer_map = {
            "product": "Product.serializers.ProductSerializer",
        }

        model_name = model._meta.model_name
        path = serializer_map.get(model_name)

        if not path:
            raise ImproperlyConfigured(
                f"No serializer defined for model '{model_name}'"
            )

        module_path, class_name = path.rsplit(".", 1)
        module = __import__(module_path, fromlist=[class_name])
        return getattr(module, class_name)



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
