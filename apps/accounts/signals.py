from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import User, UserProfile
import logging
from django.db.models.signals import post_save, pre_save
from apps.accounts.models import User
from apps.restaurant.models import Restaurant

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_user_verification_email(sender, instance, created, **kwargs):
    """Send verification email to ALL new users (customer + restaurant_owner)"""
    if created and not instance.email_verified:
        try:
            uidb64 = urlsafe_base64_encode(force_bytes(instance.pk))
            token = default_token_generator.make_token(instance)
            
            verification_url = reverse('accounts:verify-email', kwargs={
                'uidb64': uidb64, 
                'token': token
            })
            full_url = f"http://localhost:8000{verification_url}"
            
            role_text = "Customer" if instance.role == 'customer' else "Restaurant Owner"
            send_mail(
                f"✅ Verify Your SmartDine {role_text} Account!",
                f"Hi {instance.first_name or instance.username},\n\n"
                f"Please verify your email: {full_url}\n\n"
                f"Thanks,\nSmartDine Team",
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False
            )
            logger.info(f"Verification email sent to {instance.email} ({role_text})")
        except Exception as e:
            logger.error(f"Email failed for {instance.email}: {e}")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create UserProfile"""
    if created:
        UserProfile.objects.get_or_create(user=instance)


