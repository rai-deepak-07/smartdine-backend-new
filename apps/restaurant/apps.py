from django.apps import AppConfig

class RestaurantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.restaurant'
    
    def ready(self):
        import restaurant.signals  # Import signals
