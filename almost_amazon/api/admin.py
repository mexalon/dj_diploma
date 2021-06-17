from django.contrib import admin
from .models import Order, Product, ProductReview, ProductCollection, Position


class PositionInline(admin.TabularInline):
    model = Position
    extra = 1


class CollectinInline(admin.TabularInline):
    model = ProductCollection.collection_items.through
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (PositionInline,)

    ordering = ('-created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    ordering = ('id',)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    exclude = ('author',)


@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    exclude = ('collection_items',)
    inlines = (CollectinInline,)

# @admin.register(Position)
# class PositionAdmin(admin.ModelAdmin):
#     pass
