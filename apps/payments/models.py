from django.db import models
from django.utils import timezone
from datetime import timedelta

'''
class PlatformSubscription(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('pending', 'Pending'), 
                     ('expired', 'Expired'), ('cancelled', 'Cancelled')]
    
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='subscriptions')
    plan_type = models.CharField(max_length=20, choices=[('basic', 'Basic'), ('premium', 'Premium')])
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=100, blank=True)  # Razorpay order_id
    
    def save(self, *args, **kwargs):
        if self.end_date < timezone.now().date():
            self.status = 'expired'
            self.restaurant.annual_fee_status = 'overdue'
            self.restaurant.is_visible_to_users = False
            self.restaurant.save()
        super().save(*args, **kwargs)
'''



from django.db import models
from django.utils import timezone
from decimal import Decimal
from apps.restaurant.models import Restaurant

class MockPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='UPI')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.restaurant.res_name} - ₹{self.amount} - {self.status}"
