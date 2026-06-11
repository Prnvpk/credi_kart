from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'shopkeeper', 'credit_limit', 'outstanding_balance', 'city')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

# Register your models here.
