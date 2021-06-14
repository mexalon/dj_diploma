from django.contrib import admin
from .models import Orders, Products, ProductReviews, ProductCollections, Cart


class CartInline(admin.TabularInline):
    model = Cart
    extra = 1


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    inlines = (CartInline,)
    exclude = ('client',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    ...
    # inlines = (CartInline,)


@admin.register(ProductReviews)
class ProductReviewsAdmin(admin.ModelAdmin):
    exclude = ('author',)


@admin.register(ProductCollections)
class ProductCollectionsAdmin(admin.ModelAdmin):
    pass


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     pass
