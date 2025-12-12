from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path(r'page/(?P<pk>[-\w]+)/', views.page, name="page"),
]