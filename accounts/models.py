from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    SHOPKEEPER = 'shopkeeper'
    CUSTOMER = 'customer'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (SHOPKEEPER, 'Shopkeeper'),
        (CUSTOMER, 'Customer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_platform_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    @property
    def is_shopkeeper(self):
        return self.role == self.SHOPKEEPER

    @property
    def is_customer(self):
        return self.role == self.CUSTOMER


class Shopkeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shopkeeper_profile')
    shop_name = models.CharField(max_length=120)
    business_registration = models.CharField(max_length=80, blank=True)
    licence_document = models.FileField(upload_to='shopkeeper_licences/', blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    city = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name

