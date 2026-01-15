from djongo import models

class Table(models.MongoModel):
    STATUS_CHOICES = [
        ('available', 'Available'), ('reserved', 'Reserved'), 
        ('occupied', 'Occupied'), ('completed', 'Completed'), ('cleaning', 'Cleaning')
    ]
    
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, 
                                  related_name='tables')
    table_number = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    class Meta:
        unique_together = ['restaurant', 'table_number']
