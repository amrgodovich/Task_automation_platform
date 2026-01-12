from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin


class UserProfileAdmin(UserAdmin):
    model = UserProfile
    list_display = ['username', 'email', 'is_staff', 'is_active', 'is_project_manager']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Permissions', {'fields': ('is_project_manager','profile_picture')}),
    )
    readonly_fields = ['created_at']

# Register your models here.
admin.site.register(UserProfile,UserProfileAdmin)