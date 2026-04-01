from django.contrib import admin
from .models import Product, Warehouse, StockMovement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "sku", "category", "quantity", "reorder_level", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "sku", "category"]

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "capacity", "utilization", "manager", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "location", "manager"]

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ["product_name", "warehouse", "movement_type", "quantity", "reference", "created_at"]
    list_filter = ["movement_type"]
    search_fields = ["product_name", "warehouse", "reference"]
