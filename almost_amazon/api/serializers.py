from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Order, Product, ProductReview, ProductCollection, Position


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer для товара."""
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'price',)


class PositionSerializer(serializers.Serializer):
    """Serializer для позиции."""

    product_id = PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)

    amount = serializers.IntegerField(min_value=1, default=1)

    # class Meta:
    #     model = Position
    #     fields = ('product_id', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    """Serializer для заказа."""
    client = UserSerializer(
        read_only=True,
    )

    positions = PositionSerializer(many=True)

    total = serializers.DecimalField(
        read_only=True,
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        model = Order
        fields = ('id', 'client', 'positions', 'total', 'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["client"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        # user = self.context["request"].user
        #
        # if data.get('status') == 'OPEN' and adv_open >= 10:
        #     raise serializers.ValidationError(f"{user} уже создал {adv_open} открытых обьявлений")
        return data


class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer для отзыва."""
    stars = serializers.IntegerField(
        min_value=0,
        max_value=5,
    )

    class Meta:
        model = ProductReview
        fields = ('id', 'author', 'product_id', 'stars', 'created_at')

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class ProductCollectionSerializer(serializers.ModelSerializer):
    """Serializer для подборки."""

    class Meta:
        model = ProductCollection
        fields = ('id', 'title', 'collection_items', 'created_at')
