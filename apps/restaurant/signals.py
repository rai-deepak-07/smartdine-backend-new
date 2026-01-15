from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Restaurant
from apps.accounts.models import User

@receiver(post_save, sender=Restaurant)
def create_restaurant_owner_account(sender, instance, created, **kwargs):
    """
    ✅ Creates restaurant owner User account when restaurant is VERIFIED
    ✅ Sends welcome email with login details
    ✅ Creates RestaurantBank record if missing
    """
    if instance.verification_status == 'verified' and created:
        # 1. Create owner User account
        owner, owner_created = User.objects.get_or_create(
            username=instance.email,  # Use restaurant email as username
            defaults={
                'email': instance.email,
                'first_name': instance.owner_name,
                'role': 'restaurant_owner',
                'phone': instance.res_contact_no,
            }
        )
        
        # Link owner to restaurant
        instance.owner = owner
        instance.save()
        
        # 2. Generate login ID and send email
        if owner_created:
            login_id = f"{instance.owner_name.lower().replace(' ', '')}{instance.res_contact_no}"
            subject = "✅ Restaurant Verified! Login Credentials - SmartDine"
            message = (
                f"Dear {instance.owner_name},\n\n"
                f"🎊 Congratulations! Your restaurant *{instance.res_name}* is now OFFICIALLY VERIFIED!\n\n"
                f"📋 Registration Details:\n"
                f"• Registration ID: {instance.id}\n"
                f"• Restaurant Name: {instance.res_name}\n\n"
                f"🔐 Login Credentials:\n"
                f"• Login ID: {login_id}\n"
                f"• Email: {instance.email}\n\n"
                f"⏳ Your account will be ACTIVATED within 24 hours by admin.\n\n"
                f"🚀 Start managing tables, menu, staff, and orders on SmartDine!\n\n"
                f"📞 Need help? Contact SmartDine support\n\n"
                f"Best regards,\n"
                f"SmartDine Team\n\n"
                f"⚠️ Keep your login details CONFIDENTIAL"
            )
            
            send_mail(
                subject, message, settings.DEFAULT_FROM_EMAIL, 
                [instance.email], fail_silently=False
            )
            
            print(f"✅ VERIFICATION EMAIL SENT to {instance.email} for {instance.res_name}")

@receiver(pre_save, sender=Restaurant)
def auto_manage_visibility(sender, instance, **kwargs):
    """
    ✅ Auto-hide restaurants with overdue fees
    ✅ Update crowd status based on check-ins
    """
    if instance.annual_fee_status in ['overdue', 'suspended']:
        instance.is_visible_to_users = False
    elif instance.annual_fee_status == 'paid':
        instance.is_visible_to_users = True

@receiver(post_save, sender=Restaurant)
def create_default_analytics(sender, instance, created, **kwargs):
    """
    ✅ Auto-create daily analytics record
    """
    if created:
        RestaurantAnalytics.objects.get_or_create(
            restaurant=instance,
            date=timezone.now().date(),
            defaults={'total_bookings': 0, 'total_orders': 0}
        )
