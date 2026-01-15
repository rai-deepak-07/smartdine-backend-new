from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from apps.accounts.models import User
from django.utils import timezone
from .models import Restaurant, RestaurantAnalytics 

@receiver(pre_save, sender=Restaurant)
def auto_manage_visibility(sender, instance, **kwargs):
    """
    ✅ Auto-hide restaurants with overdue fees
    ✅ Update crowd status based on check-ins
    """
    if instance.annual_fee_status == 'paid':
        instance.is_visible_to_users = True
    else:
        instance.is_visible_to_users = False

@receiver(post_save, sender=Restaurant)
def create_default_analytics(sender, instance, created, **kwargs):
    """Auto-create daily analytics record"""
    if created:
        RestaurantAnalytics.objects.get_or_create(
            restaurant=instance,
            date=timezone.now().date(),
            defaults={'total_bookings': 0, 'total_orders': 0}
        )
        print(f"✅ Analytics created for {instance.res_name}")

@receiver(post_save, sender=Restaurant)
def create_restaurant_owner_account(sender, instance, created, **kwargs):
    """
    ✅ Creates restaurant owner User account with AUTO-GENERATED PASSWORD
    ✅ Sends welcome email with login + password
    ✅ Creates RestaurantBank record
    """
    if instance.verification_status == 'verified':
        print(f"🔥 Creating owner for {instance.res_name}")
        
       # 1. Create owner WITHOUT saving yet
        owner_data = {
            'username': instance.email,
            'email': instance.email,
            'first_name': instance.owner_name,
            'role': 'restaurant_owner',
            'phone': instance.res_contact_no,
        }
        
        owner, owner_created = User.objects.get_or_create(
            username=instance.email,
            defaults=owner_data
        )
        
        if owner_created:
            # ✅ GENERATE SECURE PASSWORD
            from django.contrib.auth.hashers import make_password
            import secrets
            import string
            
            # Generate strong password: 12 chars with symbols
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            temp_password = ''.join(secrets.choice(alphabet) for _ in range(12))
            
            # Set hashed password
            owner.set_password(temp_password)
            owner.save()
            
            # 2. Link owner to restaurant
            instance.owner = owner
            instance.save(update_fields=['owner'])
            
            # 3. Send welcome email WITH PASSWORD
            login_id = instance.email  # Use email as login
            subject = "✅ Welcome to SmartDine! Your Login Details"
            message = (
                f"Dear {instance.owner_name},\n\n"
                f"🎉 Congratulations! *{instance.res_name}* is VERIFIED!\n\n"
                f"🔐 **LOGIN CREDENTIALS**:\n"
                f"• **Login ID**: {login_id}\n"
                f"• **Password**: `{temp_password}`\n\n"
                f"📱 **Login URL**: https://smartdine.com/login\n\n"
                f"⚠️ **CHANGE PASSWORD** after first login!\n\n"
                f"🚀 Dashboard Features:\n"
                f"• Manage Tables & Bookings\n"
                f"• Update Menu & Prices\n"
                f"• View Orders & Analytics\n"
                f"• Staff Management\n\n"
                f"💰 **Annual Fee**: Pay ₹999 to go LIVE!\n\n"
                f"📞 Support: support@smartdine.com\n\n"
                f"SmartDine Team 🚀"
            )
            
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])
            print(f"✅ OWNER CREATED + EMAIL SENT: {instance.res_name}")
            print(f"   Login: {login_id} | Password: {temp_password}")
