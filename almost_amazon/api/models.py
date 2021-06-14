from django.conf import settings
from django.db import models


class OrderStatusChoices(models.TextChoices):
    """статусы заказа"""

    NEW = "NEW", "Создан"
    IN_PROGRESS = "IN_PROGRESS", "Обработка"
    DONE = "DONE", "Завершён"


class Products(models.Model):
    """товар"""
    name = models.CharField(
        max_length=256,
        verbose_name='товар',
    )
    description = models.TextField(
        default='',
        max_length=10000,
        verbose_name='описание',
    )

    price = models.DecimalField(
        default=1,
        max_digits=10,
        decimal_places=2,
        verbose_name='цена'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class ProductReviews(models.Model):
    """отзыв к товару"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )

    product_id = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        verbose_name='товар'
    )

    text = models.TextField(
        default='',
        max_length=10000,
        verbose_name='текст отзыва',
    )

    stars = models.IntegerField(default=5, verbose_name='оценка')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('author', 'product_id')


class Orders(models.Model):
    """заказ"""
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='клиент'
    )

    order_items = models.ManyToManyField(Products, through='Cart')

    status = models.TextField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW,
        verbose_name='статус'
    )

    total = models.DecimalField(
        default=1,
        max_digits=12,
        decimal_places=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.created_at} {self.total}"


class Cart(models.Model):
    """таблица для связи заказ - товар"""
    product_id = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        verbose_name='товар',
    )
    order_id = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        verbose_name='заказ',
    )

    amount = models.IntegerField(default=1)

    class Meta:
        unique_together = ('order_id', 'product_id')

    def __str__(self):
        return f"{self.product_id} {self.amount}"


class ProductCollections(models.Model):
    """подборка продуктов от админа"""
    title = models.CharField(
        max_length=256,
        verbose_name='заголовок',
    )

    text = models.TextField(
        default='',
        max_length=10000,
        verbose_name='текст подборки',
    )

    collection_items = models.ManyToManyField(Products)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.title}"

