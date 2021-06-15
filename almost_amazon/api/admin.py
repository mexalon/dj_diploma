from django.contrib import admin
from .models import Order, Product, ProductReview, ProductCollection, Position


class PositionInline(admin.TabularInline):
    model = Position
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (PositionInline,)
    exclude = ('client',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ...
    # inlines = (CartInline,)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    exclude = ('author',)


@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass
