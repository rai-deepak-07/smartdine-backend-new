from django.db import models
from django.utils import timezone
from datetime import timedelta, time, datetime

class Booking(models.Model):
    STATUS_CHOICES = [('booked', 'Booked'), ('dinning', 'Dinning'), 
                     ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    table = models.ForeignKey('tables.Table', on_delete=models.CASCADE)
    
    booked_at = models.DateTimeField(default=timezone.now)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    booking_end_time = models.TimeField(null=True)
    number_of_guests = models.PositiveIntegerField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='booked')
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Auto-calculate end time (2 hours)
        if self.booking_time and not self.booking_end_time:
            dt = datetime.combine(self.booking_date, self.booking_time)
            end_dt = dt + timedelta(hours=2)
            self.booking_end_time = end_dt.time()
        
        # Auto-update status based on time
        now = timezone.now()
        booking_start = datetime.combine(self.booking_date, self.booking_time).replace(tzinfo=timezone.get_current_timezone())
        booking_end = datetime.combine(self.booking_date, self.booking_end_time or self.booking_time).replace(tzinfo=timezone.get_current_timezone())
        
        if self.checked_in and self.checked_out:
            self.status = 'completed'
        elif self.checked_in:
            self.status = 'dinning'
        elif now >= booking_end:
            self.status = 'cancelled'
            
        super().save(*args, **kwargs)
