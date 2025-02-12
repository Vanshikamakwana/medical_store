from django.contrib import admin
from owner.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'product_price', 'product_expiry_date', 'stock_quantity')
    search_fields = ('product_name', 'product_des')
    list_filter = ('product_manuf_date', 'product_expiry_date', 'comp_id')
    list_editable = ('stock_quantity',)  # Admin manually update kar sake
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('product_name', 'product_price', 'stock_quantity', 'product_expiry_date')
#     list_editable = ('stock_quantity',)  # Admin manually update kar sake