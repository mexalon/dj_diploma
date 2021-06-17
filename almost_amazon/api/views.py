from django.shortcuts import redirect
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter, ProductReviewFilter, OrderFilter
from .models import Order, Product, ProductReview, ProductCollection
from .serializers import OrderSerializer, ProductSerializer, ProductReviewSerializer, ProductCollectionSerializer



class ProductViewSet(ModelViewSet):
    """ViewSet для товара."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class OrderViewSet(ModelViewSet):
    """ViewSet для заказа."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter


class ProductReviewViewSet(ModelViewSet):
    """ViewSet для отзыва."""
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductReviewFilter


class ProductCollectionViewSet(ModelViewSet):
    """ViewSet для подборки."""
    queryset = ProductCollection.objects.all()
    serializer_class = ProductCollectionSerializer


