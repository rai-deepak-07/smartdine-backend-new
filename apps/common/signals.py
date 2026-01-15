from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import *  # No models here, just utilities

# Global file cleanup mapping
FILE_FIELD_MAP = {
    'restaurant.Restaurant': ["restaurant_image", "fssai_license_url", "gst_registration_url"],
    'menu.MenuItem': ["image"],
    'staff.Staff': ["image"],
    'team.TeamMember': ["image_url"],
}

def _delete_file_if_needed(field_file):
    """Delete file from storage if not default"""
    if not field_file or not field_file.name:
        return
    if "default." in field_file.name or "default/" in field_file.name:
        return
    if default_storage.exists(field_file.name):
        default_storage.delete(field_file.name)

@receiver(pre_save)
def delete_old_files_on_change(sender, instance, **kwargs):
    """Delete old files when file fields change"""
    model_key = f"{sender.__module__.split('.')[-2]}.{sender.__name__}"
    if model_key not in FILE_FIELD_MAP:
        return
        
    if not instance.pk:
        return
        
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    
    for field_name in FILE_FIELD_MAP[model_key]:
        old_file = getattr(old_instance, field_name, None)
        new_file = getattr(instance, field_name, None)
        
        if old_file and (not new_file or old_file.name != new_file.name):
            _delete_file_if_needed(old_file)

@receiver(post_delete)
def delete_files_on_delete(sender, instance, **kwargs):
    """Delete all files when model is deleted"""
    model_key = f"{sender.__module__.split('.')[-2]}.{sender.__name__}"
    if model_key not in FILE_FIELD_MAP:
        return
        
    for field_name in FILE_FIELD_MAP[model_key]:
        file_field = getattr(instance, field_name, None)
        _delete_file_if_needed(file_field)
