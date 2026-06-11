from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('grocery', 'Grocery'),
        ('personal_care', 'Personal Care'),
        ('household', 'Household'),
        ('electronics', 'Electronics'),
        ('other', 'Other'),
    )

    shopkeeper = models.ForeignKey('accounts.Shopkeeper', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=140)
    sku = models.CharField(max_length=40, blank=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    @property
    def is_low_stock(self):
        return self.stock <= self.reorder_level

    def __str__(self):
        return self.name
