from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Shopkeeper, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_active', 'created_at')
    list_filter = ('role', 'is_approved', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('CREDI-KART Profile', {'fields': ('role', 'phone', 'address', 'is_approved')}),
    )


@admin.register(Shopkeeper)
class ShopkeeperAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'city', 'is_active', 'credit_limit', 'licence_document')
    search_fields = ('shop_name', 'user__username')

# Register your models here.
