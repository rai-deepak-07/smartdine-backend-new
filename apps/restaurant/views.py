from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Restaurant
from .serializers import RestaurantSerializer, RestaurantCreateSerializer
from rest_framework import status
from apps.accounts.models import User
from apps.geo.models import State, City
from .models import Restaurant
import logging


class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.filter(is_visible_to_users=True).select_related('city__state')
    serializer_class = RestaurantSerializer

class RestaurantRegisterView(generics.CreateAPIView):
    serializer_class = RestaurantCreateSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'states': State.objects.all(),
            'cities': City.objects.all()
        })
        return context

class RestaurantFormDataView(generics.GenericAPIView):
    def get(self, request):
        return Response({
            'states': [{'id': s.id, 'name': s.name} for s in State.objects.all()],
            'cities': [{'id': c.id, 'name': c.name, 'state': c.state.id} for c in City.objects.all()]
        })


class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'  # ✅ FIXED: Matches your custom ID field
    
    def get_queryset(self):
        return Restaurant.objects.select_related('city__state', 'owner')



from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction  # ✅ ADD THIS IMPORT
from apps.accounts.models import User
from .models import Restaurant
import logging

logger = logging.getLogger(__name__)

class RestaurantOwnerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if user.role != 'restaurant_owner':
            return Response({"error": "Restaurant Owner only"}, status=403)
        
        restaurant = user.restaurants_owned.first()
        if not restaurant:
            return Response({"error": "No restaurant"}, status=404)
        
        return Response({
            "success": True,
            "user": {
                "username": user.username,
                "first_name": user.first_name,
                "phone": user.phone or None
            },
            "restaurant": {
                "id": restaurant.id,
                "res_name": restaurant.res_name,
                "owner_name": restaurant.owner_name,
                "res_address": restaurant.res_address,
                "res_contact_no": restaurant.res_contact_no
            }
        })
    
    def patch(self, request):
        user = request.user
        if user.role != 'restaurant_owner':
            return Response({"error": "Restaurant Owner only"}, status=403)
        
        restaurant = user.restaurants_owned.first()
        if not restaurant:
            return Response({"error": "No restaurant"}, status=404)
        
        data = request.data
        
        # ✅ UPDATE BOTH MODELS AT ONCE (atomic transaction)
        with transaction.atomic():
            # Update User
            user.first_name = data.get('first_name', user.first_name)
            user.phone = data.get('phone', user.phone)
            user.save(update_fields=['first_name', 'phone'])
            
            # Update Restaurant (sync with user)
            restaurant.owner_name = data.get('owner_name', user.first_name)
            restaurant.res_contact_no = data.get('res_contact_no', user.phone)
            restaurant.res_name = data.get('res_name', restaurant.res_name)
            restaurant.res_address = data.get('res_address', restaurant.res_address)
            restaurant.save(update_fields=['owner_name', 'res_contact_no', 'res_name', 'res_address'])
        
        return Response({
            "success": True,
            "message": "✅ Profile updated!",
            "user": {
                "first_name": user.first_name,
                "phone": user.phone or None
            },
            "restaurant": {
                "res_name": restaurant.res_name,
                "owner_name": restaurant.owner_name,
                "res_contact_no": restaurant.res_contact_no
            }
        })
