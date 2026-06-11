from django.db import models
from django.utils import timezone


class CreditTransaction(models.Model):
    ACTIVE = 'active'
    PAID = 'paid'
    OVERDUE = 'overdue'
    EXTENSION_REQUESTED = 'extension_requested'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (PAID, 'Paid'),
        (OVERDUE, 'Overdue'),
        (EXTENSION_REQUESTED, 'Extension Requested'),
    )

    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='credit')
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='credit_transactions')
    shopkeeper = models.ForeignKey('accounts.Shopkeeper', on_delete=models.CASCADE, related_name='credit_transactions')
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_date = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=ACTIVE)
    reminder_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def remaining_balance(self):
        return max(self.principal_amount - self.amount_paid, 0)

    @property
    def is_overdue(self):
        return self.remaining_balance > 0 and self.due_date < timezone.localdate()

    def refresh_status(self):
        if self.remaining_balance <= 0:
            self.status = self.PAID
        elif self.is_overdue:
            self.status = self.OVERDUE
        elif self.status != self.EXTENSION_REQUESTED:
            self.status = self.ACTIVE
        self.save(update_fields=['status', 'updated_at'])

    def __str__(self):
        return f'{self.customer} - {self.remaining_balance}'

# Create your models here.
