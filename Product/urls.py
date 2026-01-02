from django.urls import path, include, re_path
from . import views
urlpatterns = [
    #Detail
    re_path(
            r'product/(?P<main_category>[-\w]+)/(?P<sub_category>[-\w]+)/(?P<slug>[-\w]+)/',
            views.product_detail, name="ProductDetail"
    ),

    re_path(
            r'product/(?P<main_category>[-\w]+)/(?P<sub_category>[-\w]+)/',
            views.product_category_list, name="ProductDetail"
    ),

    re_path(
            r'product/(?P<main_category>[-\w]+)/',
            views.product_category_list, name="ProductDetail"
    ),
    path('installment_price_calculator/', views.installment_price_calculator),

]
