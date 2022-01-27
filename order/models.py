from django.contrib.auth.models import User
from django.db import models

from menu.models import Product


class Order(models.Model): # заказ
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order Id: {self.pk} for {self.user.username}'

    @property
    def total_cost(self):
        return sum([item.get_cost()  for item in  self.items.all()])

# cheffburger = 2 -> get_cost = cheffburger.price * 2 = 12
# cola = 3 -> get_cost = cola.price * 3 = 9
# [9, 12]
# cheffburger.price * 2 + cola.price * 3 = total_cost

    class Meta:
        ordering = ('-created',)


class OrderItem(models.Model):  # продукт который уже лежит на заказе
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'OrderId: {self.order.id}, {self.product.name}'

    def get_cost(self):     # сумма одного товара
        return self.quantity * self.product.price




