from rest_framework.viewsets import ModelViewSet
from .models import Orders, Products, ProductReviews, ProductCollections
from .serializers import OrdersSerializer, ProductsSerializer, ProductReviewsSerializer, ProductCollectionsSerializer


class ProductsViewSet(ModelViewSet):
    """ViewSet для товара."""
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class OrdersViewSet(ModelViewSet):
    """ViewSet для заказа."""
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class ProductReviewsViewSet(ModelViewSet):
    """ViewSet для отзыва."""
    queryset = ProductReviews.objects.all()
    serializer_class = ProductReviewsSerializer


class ProductCollectionsViewSet(ModelViewSet):
    """ViewSet для подборки."""
    queryset = ProductCollections.objects.all()
    serializer_class = ProductCollectionsSerializer
