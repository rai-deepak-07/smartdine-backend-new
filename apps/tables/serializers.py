from rest_framework import serializers

class TableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.res_name', read_only=True)
    class Meta:
        model = Table
        fields = ['id', 'restaurant', 'restaurant_name', 'table_number', 'capacity', 'status']
