from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'customer',
        'shopkeeper',
        'payment_type',
        'payment_method',
        'payment_status',
        'total_amount',
        'status',
        'created_at',
    )
    list_filter = ('payment_type', 'payment_method', 'payment_status', 'status')
    inlines = [OrderItemInline]

# Register your models here.
