from rest_framework import serializers
from .models import *
import pandas as pd
from django.core.cache import cache
from django.db.models import F, Max, Min
from django.conf import settings



class PropertiesSerializer(serializers.ModelSerializer):
    accessory  = serializers.SerializerMethodField(read_only=True)
    final_price = serializers.SerializerMethodField(read_only=True)
    
    def get_final_price(self,obj):
        if obj.installment:
            return (((obj.length * obj.width) * obj.base_price) + obj.send_salary + obj.frame_price) * (1 - obj.normal_discount)
        else:
            return (((obj.length * obj.width) * obj.base_price) + obj.send_salary + obj.frame_price) * (1 - obj.installment_discount)
        
    class Meta:
        model = Properties
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MainCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategories
        exclude = ['slug']


class SubcategoriesSerializer(serializers.ModelSerializer):
    main  = serializers.SerializerMethodField(read_only=True)
    image  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subcategories
        fields = "__all__"
    @staticmethod
    def get_main(obj):
        main_category = {"name": obj.main.name, "slug": obj.main.slug}
        return main_category
    
    @staticmethod
    def get_image(obj):
        img_url = f"https://{settings.DOMAIN}/media/{obj.image}" if obj.image else None 
        return img_url






def add_tax(x):
    percent = 7 / 100
    addition = x['price'] * percent
    return x['price'] + addition





class ProductListNSerializer(serializers.ModelSerializer):
    properties     = PropertiesSerializer()
    main_category  = serializers.SerializerMethodField(read_only=True)
    sub_category   = serializers.SerializerMethodField(read_only=True)
    gallery        = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'name', 'image', 'slug',
            'properties',
            'main_category',
            'sub_category',
            'gallery'
        ]

    @staticmethod
    def get_gallery(obj):
        gallery = obj.gallery.values("image")
        return gallery
    
    @staticmethod
    def get_main_category(obj):
        main_category = obj.main_category
        if main_category is not None:
            main_category = {"name": main_category.name, "slug": main_category.slug , "id" : main_category.id  }
        return main_category


    @staticmethod
    def get_sub_category(obj):
        sub_category = obj.sub_category
        if sub_category is not None:
            sub_category = {"name": sub_category.name, "slug": sub_category.slug , "id" : sub_category.id}
        return sub_category





class ProductListSerializer(serializers.ModelSerializer):
    properties  = PropertiesSerializer()
    main_category_slug  = serializers.SerializerMethodField(read_only=True)
    sub_category_slug  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'name', 'image', 'slug',
            'properties', 'main_category',
            'main_category_slug',
            'sub_category_slug',
        ]


    @staticmethod
    def get_main_category_slug(obj):
        main_category = obj.main_category
        if main_category is not None:
            main_category = main_category.slug
        return main_category


    @staticmethod
    def get_sub_category_slug(obj):
        sub_category = obj.sub_category
        if sub_category is not None:
            sub_category = sub_category.slug
        return sub_category




class ProductSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField(read_only=True)
    gallery = serializers.SerializerMethodField(read_only=True)
    main_category = serializers.SerializerMethodField(read_only=True)
    sub_category = serializers.SerializerMethodField(read_only=True)
    attributes = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            '_id','name', 'image', 'price', 'count_in_stock',
            'gallery', 'slug', 'properties',
            'main_category', 'sub_category',
            'title_seo',
            'description_seo',
            'attributes',
            'description',
            # 'pre_cost_percent',
            'date_available'
        ]


    @staticmethod
    def get_image(obj):
        img =   f"https://{settings.DOMAIN}/media/{obj.image}" if obj.image else None
        return img

    @staticmethod
    def get_attributes(obj):
        attributes = obj.attributes.values("name", "comment")

        return attributes
    @staticmethod
    def get_main_category(obj):
        main_category = obj.main_category
        if main_category is not None:
            main_category = {"name": obj.main_category.name, "slug": obj.main_category.slug}
        return main_category

    @staticmethod
    def get_sub_category(obj):
        sub_category = obj.sub_category
        if sub_category is not None:
            sub_category = {"name": obj.sub_category.name, "slug": obj.sub_category.slug}
        return sub_category




    @staticmethod
    def get_gallery(obj):
        gallery = obj.gallery.values(
            'image',
            'name',
        )

        return gallery

    @staticmethod
    def get_properties(obj):
        properties = obj.properties.values()
        return properties

