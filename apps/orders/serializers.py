from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item_name', 'quantity', 'price', 'total_price', 'prepared']

class OrderSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.res_name', read_only=True)
    customer_name = serializers.CharField(source='customer.first_name', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'restaurant_name', 'customer', 'customer_name',
                 'table', 'order_time', 'order_type', 'status', 'total_amount']
