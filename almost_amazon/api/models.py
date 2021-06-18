from django.conf import settings
from django.db import models


class OrderStatusChoices(models.TextChoices):
    """статусы заказа"""

    NEW = "NEW", "Создан"
    IN_PROGRESS = "IN_PROGRESS", "Обработка"
    DONE = "DONE", "Завершён"


class Product(models.Model):
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

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name}"


class ProductReview(models.Model):
    """отзыв к товару"""
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор',
        related_name='reviwes',
    )

    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='товар'
    )

    text = models.TextField(
        default='',
        max_length=10000,
        verbose_name='текст отзыва',
    )

    stars = models.IntegerField(verbose_name='оценка')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('creator', 'product_id')
        verbose_name_plural = 'Product reviews'

    def __str__(self):
        return f"Отзыв на {self.product_id.name} от {self.creator}"


class Order(models.Model):
    """заказ"""
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='клиент'
    )

    order_items = models.ManyToManyField(Product, through='Position')

    status = models.TextField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW,
        verbose_name='статус'
    )

    total = models.DecimalField(
        default=1,
        max_digits=12,
        decimal_places=2,
        verbose_name='сумма заказа'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Создан {self.creator} {self.created_at.strftime('%c')} сумма заказа {self.total}"


class Position(models.Model):
    """таблица для связи заказ - товар"""
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='товар',
    )

    order_id = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='заказ',
        related_name='positions'
    )

    amount = models.IntegerField(
        default=1,
        verbose_name='количество'
    )

    class Meta:
        unique_together = ('order_id', 'product_id')
        verbose_name_plural = 'Positions'

    def __str__(self):
        return f"{self.product_id} {self.amount}"


class ProductCollection(models.Model):
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

    collection_items = models.ManyToManyField(Product)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Product collections'

    def __str__(self):
        return f"{self.title}"
