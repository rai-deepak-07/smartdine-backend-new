from rest_framework import serializers
from .models import Booking
from apps.restaurant.serializers import RestaurantSerializer
from apps.accounts.serializers import UserSerializer
from apps.tables.serializers import TableSerializer

class BookingSerializer(serializers.ModelSerializer):
    restaurant_detail = RestaurantSerializer(source='restaurant', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    table_detail = TableSerializer(source='table', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
