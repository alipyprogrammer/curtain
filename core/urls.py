from django.contrib import admin
from django.urls import path, include, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('User.urls')),
    path('api/ui/', include('ui.urls')),
    path('api/product/', include('Product.urls')),
]
