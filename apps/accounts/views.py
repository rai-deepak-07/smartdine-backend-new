from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from apps.restaurant.models import Restaurant
from .models import User

class UserRegisterView(generics.CreateAPIView):
    def post(self, request):
        return Response({"message": "User registration - WIP"})

class UserLoginView(generics.GenericAPIView):
    def post(self, request):
        return Response({"message": "User login - WIP"})

class UserProfileView(generics.RetrieveAPIView):
    def get(self, request):
        return Response({"message": "User profile - WIP"})
    

class RestaurantOwnerLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(username=email, password=password)
        if user and user.role == 'restaurant_owner':
            refresh = RefreshToken.for_user(user)
            restaurant = Restaurant.objects.get(owner=user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'name': user.first_name,
                    'role': user.role,
                    'email': user.email
                },
                'restaurant': {
                    'id': restaurant.id,
                    'name': restaurant.res_name,
                    'status': restaurant.annual_fee_status,
                    'visible': restaurant.is_visible_to_users
                }
            })
        
        return Response({"error": "Invalid credentials"}, status=401)

