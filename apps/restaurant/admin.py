from django.contrib import admin
from apps.restaurant import models

# Register your models here.
admin.site.register(models.Restaurant)
admin.site.register(models.RestaurantBank)
admin.site.register(models.RestaurantAnalytics)