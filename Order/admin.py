from django.contrib import admin
from .models import  *


class FactorAdmin(admin.ModelAdmin):
    list_display = ["name", "status_code" ]
    search_fields = ['name', "status_code"]
    list_filter = ["status_code"]
    list_per_page = 20

class FactorItemShipAdmin(admin.ModelAdmin):
    list_display = ["factor", "item" ]
    search_fields = ["factor", "item" ]
    list_per_page = 20


class FactorItemAdmin(admin.ModelAdmin):
    list_display = [ "id", "product" ]
    search_fields = ["id", "product" ]
    list_per_page = 20





admin.site.register(Factor, FactorAdmin)
admin.site.register(Agency)
admin.site.register(Type)
admin.site.register(PropertyItem)
admin.site.register(FactorItem, FactorItemAdmin)
admin.site.register(FactorItemShip, FactorItemShipAdmin)
admin.site.register(Card)
admin.site.register(CodeFactor)
admin.site.register(ValidateFactor)
