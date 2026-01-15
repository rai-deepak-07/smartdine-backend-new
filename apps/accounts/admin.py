from django.contrib import admin
from apps.accounts.models import User, UserProfile, PasswordResetToken, LoyaltyTransaction

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'role', 'phone']
    list_filter = ['role', 'is_active']
    
    def get_readonly_fields(self, request, obj=None):
        # ✅ MAKE PASSWORD READ-ONLY in admin
        if obj:  # Editing existing user
            return ['password']
        return []
    
    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if obj:
            fields.append('password')  # Show but read-only
        return fields

admin.site.register(UserProfile)
admin.site.register(PasswordResetToken)
admin.site.register(LoyaltyTransaction)