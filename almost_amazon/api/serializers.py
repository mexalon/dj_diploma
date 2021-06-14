from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Orders, Products, ProductReviews, ProductCollections, Cart


class UsersSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class OrdersSerializer(serializers.ModelSerializer):
    """Serializer для заказа."""
    client = UsersSerializer(
        read_only=True,
    )

    total = serializers.DecimalField(
        read_only=True,
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        model = Orders
        fields = ('id', 'client', 'total', 'status', 'created_at',)

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


class ProductsSerializer(serializers.ModelSerializer):
    """Serializer для товара."""
    price = serializers.DecimalField(
        read_only=True,
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        model = Products
        fields = ('id', 'name', 'price',)


class ProductReviewsSerializer(serializers.ModelSerializer):
    """Serializer для отзыва."""
    stars = serializers.IntegerField(
        min_value=0,
        max_value=5,
    )

    class Meta:
        model = ProductReviews
        fields = ('id', 'author', 'product_id', 'stars', 'created_at')

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    """Serializer для корзины."""
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = Cart
        fields = '__all__'


class ProductCollectionsSerializer(serializers.ModelSerializer):
    """Serializer для подборки."""

    class Meta:
        model = ProductCollections
        fields = ('id', 'title', 'collection_items', 'created_at')
