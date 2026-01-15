from django.db import models

# Create your models here.
from djongo import models

class State(models.MongoModel):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class City(models.MongoModel):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    
    class Meta:
        unique_together = ['name', 'state']
        

