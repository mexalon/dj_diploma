from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Order, Product, ProductReview, ProductCollection, Position


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email')


class ProductSerializer(serializers.ModelSerializer):
    """Serializer для товара."""
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price',)

    def validate_price(self, data):
        if data <= 0:
            raise serializers.ValidationError("Цена не может быть нулевой или отрицательной")

        return data


class PositionSerializer(serializers.Serializer):
    """Serializer для позиции."""
    product_id = PrimaryKeyRelatedField(queryset=Product.objects.all())
    amount = serializers.IntegerField(min_value=1, default=1)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer для заказа."""
    creator = UserSerializer(
        read_only=True,
    )
    positions = PositionSerializer(many=True, required=True)
    total = serializers.DecimalField(
        read_only=True,
        max_digits=12,
        decimal_places=2,
    )


    class Meta:
        model = Order
        fields = ('id', 'creator', 'positions', 'total', 'status', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        pos = validated_data.pop('positions')
        prods = [{'p': entry.get('product_id'), 'a': entry.get('amount')} for entry in pos]

        total = 0  # вычисление общей цены
        for item in prods:
            total += item['p'].price * item['a']

        validated_data["total"] = total

        order = super().create(validated_data)
        [
            Position.objects.create(
                order_id=order,
                product_id=item['p'],
                amount=item['a']
            )
            for item in prods
        ]
        return order

    def update(self, instance, validated_data):
        pos = validated_data.pop('positions', False)
        if pos:
            prods = [{'p': entry.get('product_id'), 'a': entry.get('amount', 1)} for entry in pos]

            total = 0  # пересчёт общей цены
            for item in prods:
                total += item['p'].price * item['a']

            validated_data["total"] = total

            [old_pos.delete() for old_pos in instance.positions.all()]
            # не знаю, как тут лучше поступить. Удалил всё что было и заново создал новые связи

            [
                Position.objects.create(
                    order_id=instance,
                    product_id=item['p'],
                    amount=item['a']
                )
                for item in prods
            ]

        instance = super().update(instance, validated_data)
        return instance

    def validate_positions(self, data):
        if not data:
            raise serializers.ValidationError("Заказ не может быть пустым")

        return data


class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer для отзыва."""
    creator = UserSerializer(
        read_only=True,
    )

    product_id = PrimaryKeyRelatedField(queryset=Product.objects.all())

    stars = serializers.IntegerField(
        min_value=0,
        max_value=5,
        default=5,
    )

    class Meta:
        model = ProductReview
        fields = ('id', 'creator', 'product_id', 'text', 'stars', 'created_at')

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate_product_id(self, value):
        if value in [revs.product_id for revs in self.context["request"].user.reviwes.only('product_id').all()]:
            raise serializers.ValidationError("Вы уже сделали отзыв на этот продукт")
        return value


class ProductCollectionSerializer(serializers.ModelSerializer):
    """Serializer для подборки."""

    class Meta:
        model = ProductCollection
        fields = ('id', 'title', 'text', 'collection_items', 'created_at')
