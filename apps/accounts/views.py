from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .models import User, UserProfile, PasswordResetToken
from .serializers import (
    UserRegisterSerializer, PasswordResetRequestSerializer, 
    PasswordResetConfirmSerializer, CompleteUserUpdateSerializer, 
    UserProfileFullSerializer
)
from apps.restaurant.models import Restaurant
import secrets


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UniversalLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "❌ Invalid credentials"}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({"error": "❌ Account inactive"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if not user.email_verified and user.role == 'customer':
            return Response({"error": "❌ Email not verified!"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        
        user_data = {
            "user_pk": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "phone": user.phone or None,
            "role": user.role,
            "email_verified": user.email_verified,
            "is_active": user.is_active,
            "date_joined": user.date_joined.isoformat(),
            "restaurant_pk": None,
            "restaurant": None
        }
        
        if user.role == 'restaurant_owner':
            try:
                restaurants = user.restaurants_owned.filter(verification_status='verified')
                if not restaurants.exists():
                    restaurants = user.restaurants_owned.all()
                
                if restaurants.exists():
                    restaurant = restaurants.first()
                    user_data.update({
                        "restaurant_pk": restaurant.id,
                        "restaurant": {
                            "id": restaurant.id,
                            "res_name": restaurant.res_name,
                            "res_address": restaurant.res_address,
                            "res_contact_no": restaurant.res_contact_no,
                            "owner_name": restaurant.owner_name,
                            "email": restaurant.email,
                            "state": restaurant.state.name if restaurant.state else None,
                            "city": restaurant.city.name if restaurant.city else None,
                            "verification_status": restaurant.verification_status,
                            "is_open": restaurant.is_open,
                            "crowd_status": restaurant.crowd_status,
                        }
                    })
            except Exception as e:
                print(f"Restaurant error: {e}")
        
        return Response({
            "success": True,
            "tokens": {"refresh": str(refresh), "access": access},
            "user": user_data
        })


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                # ✅ CRITICAL: Generate & SAVE password if missing
                if not user.auto_generated_password:
                    auto_password = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%") for _ in range(12))
                    user.auto_generated_password = auto_password
                    user.set_password(auto_password)
                
                # ✅ ACTIVATE USER
                user.email_verified = True
                user.is_active = True
                user.save()
                
                self.send_credentials_email(user)
                
                return Response({
                    "success": True,
                    "message": f"✅ {user.role.title()} account activated! Check email for login.",
                    "user": {"username": user.username, "email": user.email, "role": user.role}
                })
            return Response({"error": "❌ Invalid/expired link"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "❌ User not found"}, status=404)
        except Exception:
            return Response({"error": "❌ Invalid link"}, status=400)

    
    def send_credentials_email(self, user):
        auto_password = getattr(user, 'auto_generated_password', None)
        if not auto_password:
            auto_password = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%") for _ in range(12))
            user.auto_generated_password = auto_password
            user.set_password(auto_password)
            user.save()
        
        send_mail(
            "🎉 SmartDine - Login Credentials Ready!",
            f"""✅ Account ACTIVATED!
👤 Username: {user.username}
📧 Email: {user.email}
🔑 Password: `{auto_password}`
📱 Login: http://localhost:8000/api/v1/accounts/login/
⚠️ Change password after first login!""",
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            PasswordResetToken.objects.filter(user=user).delete()
            token_str = secrets.token_urlsafe(64)
            PasswordResetToken.objects.create(user=user, token=token_str)
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"http://localhost:8000/api/v1/accounts/reset-password-confirm/{uidb64}/{token}/"
            
            send_mail(
                "🔐 Reset Your SmartDine Password",
                f"Click to reset: {reset_url}\nToken expires in 10 minutes.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )
            
            return Response({
                "success": True,
                "message": "✅ Password reset email sent!",
                "data": {"email": user.email, "expires_in": 600}
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                return Response({"success": True, "message": "Token valid!"})
            return Response({"error": "❌ Invalid/expired token"}, status=400)
        except:
            return Response({"error": "❌ Invalid token"}, status=400)
    
    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                
                if default_token_generator.check_token(user, token):
                    user.set_password(serializer.validated_data['password'])
                    user.save()
                    PasswordResetToken.objects.filter(user=user).update(is_used=True)
                    return Response({"success": True, "message": "✅ Password reset!"})
                return Response({"error": "❌ Invalid/expired token"}, status=400)
            except:
                return Response({"error": "❌ User not found"}, status=400)
        return Response(serializer.errors, status=400)


class CompleteUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': getattr(user, 'phone', ''),
            'role': getattr(user, 'role', 'customer'),
            'profile': {
                'address': profile.address,
                'pincode': profile.pincode,
                'city': profile.city
            }
        }
        return Response(data)
    
    def patch(self, request):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        
        update_data = request.data
        user.first_name = update_data.get('first_name', user.first_name)
        user.last_name = update_data.get('last_name', user.last_name)
        user.phone = update_data.get('phone', user.phone)
        user.save()
        
        profile.address = update_data.get('address', profile.address)
        profile.pincode = update_data.get('pincode', profile.pincode)
        profile.city = update_data.get('city', profile.city)
        profile.save()
        
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': getattr(user, 'phone', ''),
            'role': getattr(user, 'role', 'customer'),
            'profile': {
                'address': profile.address,
                'pincode': profile.pincode,
                'city': profile.city
            }
        }
        return Response(data)