from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from apps.accounts.models import User
from django.utils import timezone
from .models import Restaurant, RestaurantAnalytics 
import secrets
import string
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Restaurant)
def auto_manage_visibility(sender, instance, **kwargs):
    """Auto-hide restaurants with overdue fees"""
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


@receiver(post_save, sender=Restaurant)
def create_restaurant_owner_account(sender, instance, created, **kwargs):
    """
    ✅ Creates restaurant owner IMMEDIATELY on restaurant creation
    ✅ Sends verification email (not welcome email)
    """
    if created:  # ✅ CHANGED: Fires on EVERY restaurant creation
        try:
            # ✅ CREATE OWNER USER (inactive)
            auto_password = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%") for _ in range(12))
            
            owner_data = {
                'username': instance.email,
                'email': instance.email,
                'first_name': instance.owner_name,
                'phone': instance.res_contact_no,
                'role': 'restaurant_owner',
                'is_active': False,
                'email_verified': False,
                'auto_generated_password': auto_password,
                'password': auto_password  # Gets hashed by create_user
            }
            
            owner, created = User.objects.get_or_create(
                username=instance.email,
                defaults=owner_data
            )
            
            if created:
                owner.set_password(auto_password)
                owner.save()
                
                # ✅ LINK OWNER TO RESTAURANT
                instance.owner = owner
                instance.save(update_fields=['owner'])
                
                logger.info(f"✅ Restaurant owner created: {instance.res_name}")
                
        except Exception as e:
            logger.error(f"❌ Owner creation failed for {instance.res_name}: {e}")


@receiver(post_save, sender=Restaurant)
def send_restaurant_verification_email(sender, instance, created, **kwargs):
    """Send verification email when restaurant owner created"""
    if created and instance.owner and not instance.owner.email_verified:
        try:
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            from django.contrib.auth.tokens import default_token_generator
            from django.urls import reverse
            
            uidb64 = urlsafe_base64_encode(force_bytes(instance.owner.pk))
            token = default_token_generator.make_token(instance.owner)
            
            verification_url = reverse('accounts:verify-email', kwargs={
                'uidb64': uidb64, 
                'token': token
            })
            full_url = f"http://localhost:8000{verification_url}"
            
            send_mail(
                "✅ Verify Your SmartDine Restaurant Account!",
                f"Hi {instance.owner_name},\n\n"
                f"Your restaurant *{instance.res_name}* is registered!\n\n"
                f"Click to activate: {full_url}\n\n"
                f"SmartDine Team",
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False
            )
            logger.info(f"✅ Verification email sent for {instance.res_name}")
            
        except Exception as e:
            logger.error(f"❌ Verification email failed for {instance.res_name}: {e}")
