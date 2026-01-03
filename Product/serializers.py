from rest_framework import serializers
from .models import *
import pandas as pd
from django.core.cache import cache
from django.db.models import F, Max, Min
from django.conf import settings
from django.db.models import Avg, Count

from django.db.models import Value
from django.db.models.functions import Concat


class PropertiesSerializer(serializers.ModelSerializer):
    # accessory  = serializers.SerializerMethodField(read_only=True)
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
        img_url = f"http://{settings.DOMAIN}/media/{obj.image}" if obj.image else None 
        return img_url






def add_tax(x):
    percent = 7 / 100
    addition = x['price'] * percent
    return x['price'] + addition





class ProductListNSerializer(serializers.ModelSerializer):
    properties  = serializers.SerializerMethodField(read_only=True)
    main_category  = serializers.SerializerMethodField(read_only=True)
    sub_category   = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    gallery        = serializers.SerializerMethodField(read_only=True)


    price_per_meter = serializers.SerializerMethodField(read_only=True)
    final_price     = serializers.SerializerMethodField(read_only=True)

    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    

    class Meta:
        model = Product
        fields = [
            'name', 'image', 'slug',
            'properties',
            'main_category',
            'sub_category',
            'gallery',


            'price_per_meter',
            'final_price',

            'average_rating',
            'reviews_count',
            'reviews'
        ]


   @staticmethod
    def get_image(obj):
        img =   f"http://{settings.DOMAIN}/media/{obj.image}" if obj.image else None
        return img


    def get_final_price(self, obj):
        obj = obj.properties.first()
        if obj.installment:
            return (((obj.length * obj.width) * obj.base_price) + obj.send_salary + obj.frame_price) * (1 - obj.normal_discount)
        else:
            return (((obj.length * obj.width) * obj.base_price) + obj.send_salary + obj.frame_price) * (1 - obj.installment_discount)


    def get_price_per_meter(self, obj):
        price = obj.properties.first().base_price
        return price


    def get_average_rating(self, obj):
        avg = obj.reviews_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else 0
    
    def get_reviews_count(self, obj):
        return obj.reviews_set.count()

    def get_reviews(self, obj):
        reviews = obj.reviews_set.all()
        return ReviewSerializer(reviews, many=True).data

    @staticmethod
    def get_gallery(obj):
        gallery = obj.gallery.values("image")
        return gallery
    

    @staticmethod
    def get_properties(obj):
        properties = PropertiesSerializer(obj.properties, many=True).data
        return properties
    


    
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


class ReviewSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Reviews
        fields = ['_id', 'name', 'rating', 'comment']
    
    def get_name(self, obj):
        name = obj.user.name
        return name

class ProductSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField(read_only=True)
    gallery = serializers.SerializerMethodField(read_only=True)
    main_category = serializers.SerializerMethodField(read_only=True)
    sub_category = serializers.SerializerMethodField(read_only=True)
    attributes = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    
    price_per_meter = serializers.SerializerMethodField(read_only=True)
    final_price     = serializers.SerializerMethodField(read_only=True)

    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            '_id','name', 'image', 'count_in_stock',
            'gallery', 'slug', 'properties',
            'main_category', 'sub_category',
            'title_seo',
            'description_seo',
            'attributes',
            'description',
            # 'pre_cost_percent',
            'date_available',

            'price_per_meter',
            'final_price',

            'average_rating',
            'reviews_count',
            'reviews'
        ]

        


    def get_final_price(self, obj):
        obj = obj.properties.first()
        if obj.installment:
            return (((obj.length * obj.width) * obj.base_price) + obj.send_salary + obj.frame_price) * (1 - obj.normal_discount)
        else:
            return (((obj.length * obj.width) * obj.base_price) + obj.send_salary + obj.frame_price) * (1 - obj.installment_discount)


    def get_price_per_meter(self, obj):
        price = obj.properties.first().base_price
        return price


    def get_average_rating(self, obj):
        avg = obj.reviews_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else 0
    
    def get_reviews_count(self, obj):
        return obj.reviews_set.count()

    def get_reviews(self, obj):
        reviews = obj.reviews_set.all()
        return ReviewSerializer(reviews, many=True).data


    @staticmethod
    def get_image(obj):
        img =   f"http://{settings.DOMAIN}/media/{obj.image}" if obj.image else None
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
        BASE_URL = "http://curtain.linooxel.com:5042/media/"

        gallery = obj.gallery.values('image', 'name')

        return [
            {
                'image': f"{BASE_URL}{item['image']}" if item['image'] else None,
                'name': item['name']
            }
            for item in gallery
        ]

    @staticmethod
    def get_properties(obj):
        properties = obj.properties.values()
        return properties

