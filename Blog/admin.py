from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(MainCategories)
admin.site.register(Subcategories)
admin.site.register(Tag)
admin.site.register(Blog)