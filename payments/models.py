from django.db import models


class Payment(models.Model):
    CASH = 'cash'
    UPI = 'upi'
    CARD = 'card'
    BANK = 'bank'
    METHOD_CHOICES = ((CASH, 'Cash'), (UPI, 'UPI'), (CARD, 'Card'), (BANK, 'Bank Transfer'))

    credit = models.ForeignKey('credits.CreditTransaction', on_delete=models.CASCADE, related_name='payments')
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='payments')
    shopkeeper = models.ForeignKey('accounts.Shopkeeper', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default=CASH)
    reference = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-paid_at']

    def __str__(self):
        return f'{self.amount} for {self.credit_id}'


