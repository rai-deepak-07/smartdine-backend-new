from rest_framework import serializers

class StaffSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.res_name', read_only=True)
    
    class Meta:
        model = Staff
        fields = '__all__'
