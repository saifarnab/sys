from django.contrib import admin
from .models import EventType, EventBranchVenue, EventCategory, EventSubCategory


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at', 'status']


class EventBranchVenueAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'contact_no', 'created_at', 'updated_at', 'status']


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at', 'status']


class EventSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'created_at', 'updated_at', 'status']


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(EventBranchVenue, EventBranchVenueAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(EventSubCategory, EventSubCategoryAdmin)

