from django.contrib import admin

from .models import CreditTransaction


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'shopkeeper', 'principal_amount', 'amount_paid', 'due_date', 'status')
    list_filter = ('status', 'due_date')

# Register your models here.
