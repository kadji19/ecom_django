from django.contrib import admin

from .models import Customer, Product, Cart, CartItem

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'address', 'tel', 'country')
    search_fields = ('user__username', 'name', 'tel')

admin.site.register(Customer, CustomerAdmin)


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
 list_display = ('id', 'name', 'description', 'price', 'product_image')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'get_total_price')
    inlines = [CartItemInline]

admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'size', 'color', 'quantity', 'added_at')
    list_filter = ('cart', 'product', 'size', 'color')

admin.site.register(CartItem, CartItemAdmin)