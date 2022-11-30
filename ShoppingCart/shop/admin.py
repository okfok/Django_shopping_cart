from django.contrib import admin

from .models import Item, CartItem, Cart


class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 3


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(Cart, CartAdmin)
