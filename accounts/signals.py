from django.db.models.signals import post_save
from django.dispatch import receiver

from customers.models import Customer
from .models import User


@receiver(post_save, sender=User)
def create_role_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.CUSTOMER:
        Customer.objects.get_or_create(user=instance)
