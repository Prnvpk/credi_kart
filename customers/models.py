from django.conf import settings
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    shopkeeper = models.ForeignKey(
        'accounts.Shopkeeper',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers',
    )
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=5000)
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    city = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# Create your models here.
