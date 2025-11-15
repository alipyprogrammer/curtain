from rest_framework import serializers
from .models import *




class MainCategoriesSerializer(serializers.ModelSerializer):
    class Meta:

        model = MainCategories
        exclude = ['slug']


class SubcategoriesSerializer(serializers.ModelSerializer):
    main  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subcategories
        fields = "__all__"
    @staticmethod
    def get_main(obj):
        main_category = {"name": obj.main.name, "slug": obj.main.slug}
        return main_category



class BlogSerializer(serializers.ModelSerializer):
    main_category  = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model  = Blog
        fields = '__all__'

    @staticmethod
    def get_main_category(obj):
        category = obj.main_category
        serializer = MainCategoriesSerializer(category, many=False)
        return serializer.data

