from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('credit', 'customer', 'shopkeeper', 'amount', 'method', 'paid_at')
    list_filter = ('method',)

# Register your models here.
