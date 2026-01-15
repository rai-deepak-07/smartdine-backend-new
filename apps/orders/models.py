from django.db import models
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('preparing', 'Preparing'), 
                     ('served', 'Served'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, null=True, blank=True)
    
    order_type = models.CharField(max_length=10, choices=[('preorder', 'Pre Order'), ('order', 'Order')], default='order')
    order_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def update_total(self):
        total = sum(item.total_price for item in self.order_items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    prepared = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.menu_item and not self.price:
            self.price = self.menu_item.price
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()