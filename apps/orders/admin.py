from django.contrib import admin
from apps.orders.models import Discount, Tax, Order


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(Tax)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class DiscountAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price',)
