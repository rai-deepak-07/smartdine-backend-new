from rest_framework import serializers
from .models import Restaurant, RestaurantBank, RestaurantAnalytics
from apps.geo.models import State, City 

class RestaurantBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantBank
        fields = ['id', 'restaurant', 'upi_id', 'upi_registered_name', 'pan_no']

class RestaurantAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantAnalytics
        fields = ['id', 'restaurant', 'date', 'total_bookings', 'total_orders', 'revenue', 'avg_diners']

class RestaurantSerializer(serializers.ModelSerializer):
    # Nested related data
    city_name = serializers.CharField(source='city.name', read_only=True)
    state_name = serializers.CharField(source='city.state.name', read_only=True)
    owner_name = serializers.CharField(source='owner.first_name', read_only=True)
    
    class Meta:
        model = Restaurant
        fields = [
            'id', 'res_name', 'res_address', 'res_contact_no',
            'google_location_url', 'state_name', 'city_name', 'is_open', 'opening_time',
            'closing_time', 'owner_name', 'restaurant_image', 'fssai_license_no',
            'fssai_license_url', 'gst_registration_no', 'gst_registration_url',
            'verification_status', 'annual_fee_status', 'fee_due_date', 'is_visible_to_users',
            'current_checkedin_guests', 'total_tables', 'crowd_status', 'last_crowd_update',
            'latitude', 'longitude'
        ]
        read_only_fields = ['id', 'res_contact_no','verification_status', 'annual_fee_status',
                            'fee_due_date', 'is_visible_to_users', 'current_checkedin_guests','total_tables',
                            'last_crowd_update','latitude', 'longitude']

class RestaurantCreateSerializer(serializers.ModelSerializer):
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    
    class Meta:
        model = Restaurant
        fields = ['res_name', 'res_address', 'res_contact_no', 'google_location_url',
                 'state', 'city', 'owner_name', 'email', 'fssai_license_no', 
                 'fssai_license_url', 'gst_registration_no', 'gst_registration_url']
