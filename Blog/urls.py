from django.urls import URLPattern, path , include,re_path 
from . import views
from .views import *


urlpatterns = [ 
    #LIST
    path('blog/main-category/', MainCategoriesList.as_view() ,name='CategoryList'),
    path('blog/sub-category/', SubcategoriesList.as_view() ,name='CategoryFList'),
    path('blog/list/', BlogList.as_view() ,name='BlogList'),

    #DETAIL
    re_path(r'blog/detail/main-category/(?P<slug>[-\w]+)/' ,MainCategoriesDetail.as_view() ,name="CategoryDetail"),
    re_path(r'blog/detail/sub-category/(?P<slug>[-\w]+)/' ,SubcategoriesDetail.as_view() ,name="CategoryFDetail"),
    re_path(r'blog/detail/blog/(?P<slug>[-\w]+)/' ,BlogDetail.as_view() ,name="BlogDetail"),
]
