from django.contrib import admin
from .models import Product, Category,Cart,Order,Wishlist,Coupon


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['id']
admin.site.register(Cart)
# admin.site.register(Order)
admin.site.register(Wishlist)
admin.site.register(Coupon)