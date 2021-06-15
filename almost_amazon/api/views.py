from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.viewsets import ModelViewSet
from .models import Order, Product, ProductReview, ProductCollection
from .serializers import OrderSerializer, ProductSerializer, ProductReviewSerializer, ProductCollectionSerializer


class ProductViewSet(ModelViewSet):
    """ViewSet для товара."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(ModelViewSet):
    """ViewSet для заказа."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductReviewViewSet(ModelViewSet):
    """ViewSet для отзыва."""
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer


class ProductCollectionViewSet(ModelViewSet):
    """ViewSet для подборки."""
    queryset = ProductCollection.objects.all()
    serializer_class = ProductCollectionSerializer


