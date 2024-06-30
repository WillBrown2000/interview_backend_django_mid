from django.contrib import admin
from .models import Order, OrderTag

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','created_at')
    ordering = ('-created_at',)

@admin.register(OrderTag)
class OrderTagAdmin(admin.ModelAdmin):
    list_display = ('id',)
