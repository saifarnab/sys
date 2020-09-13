from django.contrib import admin
from .models import EventType


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at', 'status']


admin.site.register(EventType, EventTypeAdmin)
