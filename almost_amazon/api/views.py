from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter, ProductReviewFilter, OrderFilter
from .models import Order, Product, ProductReview, ProductCollection
from .serializers import OrderSerializer, ProductSerializer, ProductReviewSerializer, ProductCollectionSerializer
from .permissions import CreatorOrAdminPermission, CreatorOrAdminPermission, OrderUpdatePermission, OrderCreatePermission


class ProductViewSet(ModelViewSet):
    """ViewSet для товара."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        permissions = [AllowAny]
        if self.action in ["create", "update", "partial_update", 'destroy']:
            permissions += [IsAdminUser]

        return [p() for p in permissions]


class OrderViewSet(ModelViewSet):
    """ViewSet для заказа."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def list(self, request):
        if not request.user.is_staff:
            queryset = Order.objects.filter(creator=request.user)
        else:
            queryset = Order.objects.all()

        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action in ["list", "retrieve", ]:
            permissions += [CreatorOrAdminPermission]
        if self.action in ["create", ]:
            permissions += [OrderCreatePermission]
        if self.action in ["update", "partial_update", 'destroy']:
            permissions += [CreatorOrAdminPermission, OrderUpdatePermission]

        return [p() for p in permissions]


class ProductReviewViewSet(ModelViewSet):
    """ViewSet для отзыва."""
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductReviewFilter

    def get_permissions(self):
        permissions = [AllowAny]
        if self.action in ["create", ]:
            permissions += [IsAuthenticated]
        if self.action in ["update", "partial_update", 'destroy']:
            permissions += [CreatorOrAdminPermission]

        return [p() for p in permissions]


class ProductCollectionViewSet(ModelViewSet):
    """ViewSet для подборки."""
    queryset = ProductCollection.objects.all()
    serializer_class = ProductCollectionSerializer

    def get_permissions(self):
        permissions = [AllowAny]
        if self.action in ["create", "update", "partial_update", 'destroy']:
            permissions += [IsAdminUser]

        return [p() for p in permissions]
