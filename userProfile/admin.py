from django.contrib import admin
from .models import User, AdminProfile, OrgProfile
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'role']


class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']


class OrgProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'contact_number', 'email', 'address', 'facebook_link', 'twitter_link', 'linkedin_link', 'created_at', 'updated_at']


admin.site.register(User, CustomUserAdmin)
admin.site.register(AdminProfile, AdminProfileAdmin)
admin.site.register(OrgProfile, OrgProfileAdmin)
