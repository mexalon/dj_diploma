from django_filters import rest_framework as filters
from .models import Order, Product, ProductReview, ProductCollection, OrderStatusChoices


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    description = filters.CharFilter(field_name="description", lookup_expr="contains")
    price_from = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_to = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ('price', 'name', 'description')


class ProductReviewFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    stars_from = filters.NumberFilter(field_name="stars", lookup_expr="gte")
    stars_to = filters.NumberFilter(field_name="stars", lookup_expr="lte")

    class Meta:
        model = ProductReview
        fields = ('author', 'product_id', 'created_at', 'stars')


class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=OrderStatusChoices.choices)
    total = filters.RangeFilter()
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ('status', 'total', 'created_at', 'updated_at', 'order_items')
