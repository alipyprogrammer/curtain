from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import *
# Register your models here.


UserAdmin.fieldsets[2][1]['fields'] =(
    'type_ads',
    ##########
    'is_active',
    'is_staff',
    'is_superuser',
    'groups',
    ##########
    'name',
    'mobile',
    'manager',
    'customer',
    'blog_manager',
    'product_manager',
    'ordering_manager',
)
# UserAdmin.list_display += ('is_author','is_special_user')
admin.site.register(User, UserAdmin)
admin.site.register(Age)
admin.site.register(Address)
