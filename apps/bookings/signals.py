from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from apps.orders.models import Order

@receiver(post_save, sender=Booking)
def update_order_status_on_checkout(sender, instance, **kwargs):
    """Auto-complete orders when booking is checked out"""
    if instance.checked_out and instance.status == 'completed':
        orders = Order.objects.filter(booking=instance)
        for order in orders:
            if order.status != 'completed':
                order.status = 'completed'
                order.save()
