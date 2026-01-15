from djongo import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import os

class User(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('restaurant_owner', 'Restaurant Owner'),
        ('staff', 'Restaurant Staff'),
        ('customer', 'Customer'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True,
        validators=[RegexValidator(r'^\+?\d{10,15}$')])
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    
    loyalty_points = models.PositiveIntegerField(default=0, help_text="SmartPoints earned")
    total_earned_points = models.PositiveIntegerField(default=0)
    points_updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = False

class UserProfile(models.MongoModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=6, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
class PasswordResetToken(models.MongoModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        return (not self.is_used) and (timezone.now() - self.created_at).seconds < 600

class LoyaltyTransaction(models.MongoModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loyalty_transactions')
    points = models.IntegerField()  # Positive for earn, negative for redeem
    reason = models.CharField(max_length=100)  # "Booking", "Preorder", "Redeem"
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey('bookings.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)