from django.db import models

class Staff(models.Model):
    ROLE_CHOICES = [
        ('chef', 'Chef'), ('manager', 'Manager'), ('waiter', 'Waiter'),
        ('cleaner', 'Cleaner'), ('cashier', 'Cashier'), ('delivery', 'Delivery Boy'),
        ('other', 'Other')
    ]
    
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, 
                                  related_name='staff_members')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=True, null=True)
    
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='staff_images/')
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
