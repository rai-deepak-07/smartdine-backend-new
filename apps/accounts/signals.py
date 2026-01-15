from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User, PasswordResetToken

@receiver(post_save, sender=User)
def send_user_welcome_email(sender, instance, created, **kwargs):
    if created and instance.role == 'customer':
        subject = "Welcome to SmartDine! 🎉"
        message = (
            f"Welcome to SmartDine, {instance.first_name or instance.username}!\n\n"
            f"🎉 Your account has been created successfully. You can now:\n"
            f"• Browse restaurants near you\n"
            f"• Book tables in advance\n"
            f"• Pre-order meals and skip the queue 🍴\n\n"
            f"Email: {instance.email}\n\n"
            f"❤️ Earn SmartPoints with every booking!\n\n"
            f"Best regards,\nSmartDine Team"
        )
        send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL,
            [instance.email], fail_silently=False
        )
