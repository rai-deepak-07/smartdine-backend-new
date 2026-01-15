from djongo import models

class MenuCategory(models.MongoModel):
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, 
                                  related_name='menu_categories')
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ['restaurant', 'name']

class MenuItem(models.MongoModel):
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, 
                                  related_name='menu_items')
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    food_type = models.CharField(max_length=10, choices=[('veg', 'Veg'), ('nonveg', 'Non-Veg')], default='veg')
    image = models.ImageField(upload_to='menu_items/', blank=True)
    is_available = models.BooleanField(default=True)
    # stock_quantity = models.PositiveIntegerField(default=0)  # Added for inventory
