from django.db import models


class Order(models.Model):
    READY = 'ready'
    PAY_LATER = 'pay_later'
    PAYMENT_CHOICES = ((READY, 'Ready Payment'), (PAY_LATER, 'Pay Later'))

    UPI = 'upi'
    CARD = 'card'
    PAYMENT_METHOD_CHOICES = ((UPI, 'UPI'), (CARD, 'Card'))

    PAYMENT_PENDING = 'pending'
    PAYMENT_PAID = 'paid'
    PAYMENT_CREDIT = 'credit'
    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_PAID, 'Paid'),
        (PAYMENT_CREDIT, 'Pay Later'),
    )

    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = ((PENDING, 'Pending'), (COMPLETED, 'Completed'), (CANCELLED, 'Cancelled'))

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='orders')
    shopkeeper = models.ForeignKey('accounts.Shopkeeper', on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    payment_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=COMPLETED)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='order_items')
    product_name = models.CharField(max_length=140)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'
