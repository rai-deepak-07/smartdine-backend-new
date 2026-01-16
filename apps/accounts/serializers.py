from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import User, UserProfile, PasswordResetToken
import string
import secrets


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'phone']
    
    def create(self, validated_data):
        auto_password = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%") for _ in range(12))
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            phone=validated_data.get('phone', ''),
            password=auto_password,
            is_active=False,
            email_verified=False
        )
        user.role = 'customer'
        user.auto_generated_password = auto_password
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'phone', 'role', 
                 'loyalty_points', 'total_earned_points', 'points_updated_at']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email!")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords don't match!")
        validate_password(attrs['password'])  # Django password validation
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['address', 'pincode', 'city']


class CompleteUserUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    pincode = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)


class UserProfileFullSerializer(serializers.Serializer):  # ✅ Changed to Serializer (no profile error)
    id = serializers.IntegerField(source='id')
    username = serializers.CharField(source='username')
    email = serializers.EmailField(source='email')
    first_name = serializers.CharField(source='first_name')
    last_name = serializers.CharField(source='last_name')
    phone = serializers.CharField(source='phone')
    role = serializers.CharField(source='role')
    
    def to_representation(self, instance):
        user = instance
        try:
            profile = user.profile  # Now works with related_name='profile'
            profile_data = UserProfileSerializer(profile).data
        except:
            profile_data = {'address': '', 'pincode': '', 'city': ''}
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': getattr(user, 'phone', ''),
            'role': getattr(user, 'role', 'customer'),
            'profile': profile_data
        }

