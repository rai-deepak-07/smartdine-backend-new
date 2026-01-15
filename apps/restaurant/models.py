from djongo import models
from django.utils import timezone
from django.core.validators import RegexValidator, FileExtensionValidator
from django.contrib.auth.hashers import make_password
from datetime import time
from django.utils.html import format_html

class Restaurant(models.MongoModel):
    # Auto-generated ID
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    
    # Restaurant Info
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    res_name = models.CharField(max_length=100)
    res_address = models.TextField()
    res_contact_no = models.CharField(max_length=15, unique=True,
        validators=[RegexValidator(r'^\+?\d{10,15}$')])
    google_location_url = models.URLField(blank=True)
    
    # MISSING FIELDS FROM YOUR ORIGINAL (ADDED)
    owner_name = models.CharField(max_length=100)  # ✅ ADDED
    email = models.EmailField(unique=True)         # ✅ ADDED
    
    # Location
    state = models.ForeignKey('geo.State', on_delete=models.PROTECT)
    city = models.ForeignKey('geo.City', on_delete=models.PROTECT)
    
    # Operations
    is_open = models.BooleanField(default=True)
    opening_time = models.TimeField(default=time(10, 0))
    closing_time = models.TimeField(default=time(22, 0))
    
    # Owner User (for auth)
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, 
                             related_name='restaurants_owned', null=True, blank=True)
    
    # Coordinates (SIMPLE - no GeoDjango)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Legal Docs
    restaurant_image = models.ImageField(upload_to='restaurants/', blank=True)
    fssai_license_no = models.CharField(max_length=30, unique=True)
    fssai_license_url = models.FileField(upload_to='fssai/', 
        validators=[FileExtensionValidator(['pdf'])])
    gst_registration_no = models.CharField(max_length=30, unique=True)
    gst_registration_url = models.FileField(upload_to='gst/',
        validators=[FileExtensionValidator(['pdf'])])
    
    # Platform Fees + Visibility
    verification_status = models.CharField(max_length=12, 
        choices=[('not_verified', 'Not Verified'), ('verified', 'Verified')], 
        default='not_verified')
    
    annual_fee_status = models.CharField(
        max_length=20, 
        choices=[('paid', 'Paid'), ('pending', 'Pending'), ('overdue', 'Overdue'), ('suspended', 'Suspended')],
        default='pending'
    )
    fee_due_date = models.DateField(null=True, blank=True)
    is_visible_to_users = models.BooleanField(default=True, help_text="Show in user feed")
    
    # Crowd Status (SIMPLE checked-in count)
    current_checkedin_guests = models.PositiveIntegerField(default=0)
    total_tables = models.PositiveIntegerField(default=0)
    crowd_status = models.CharField(max_length=10, default='empty',
        choices=[('empty','Empty'), ('low','Low'), ('busy','Busy'), ('full','Full')])
    last_crowd_update = models.DateTimeField(auto_now=True)
    
    def colored_verification_status(self):
        color = 'green' if self.verification_status == 'verified' else 'red'
        icon = '✅' if self.verification_status == 'verified' else '❌'
        return format_html(f'<span style="color: {color};">{icon} {self.get_verification_status_display()}</span>')
    
    def save(self, *args, **kwargs):
        if not self.id:
            now = timezone.now()
            date_str = now.strftime("%d%m%Y")
            name_part = (self.res_name[:6].upper() + 'X'*(6-len(self.res_name[:6])) 
                        if len(self.res_name) >= 6 else self.res_name.upper().ljust(6, 'X'))
            self.id = f"SD{name_part}{date_str}"
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class RestaurantBank(models.MongoModel):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    upi_id = models.CharField(max_length=100, unique=True)
    upi_registered_name = models.CharField(max_length=100)
    pan_no = models.CharField(max_length=10)

class RestaurantAnalytics(models.MongoModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    total_bookings = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    avg_diners = models.FloatField(default=0)
