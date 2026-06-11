from django.db import models


class Cart(models.Model):
    customer = models.OneToOneField('customers.Customer', on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return sum(item.line_total for item in self.items.select_related('product'))

    def __str__(self):
        return f'Cart #{self.pk} - {self.customer}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def line_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product} x {self.quantity}'


