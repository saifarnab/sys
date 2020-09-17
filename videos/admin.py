from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'video', 'created_at', 'updated_at', 'status']


admin.site.register(Video, VideoAdmin)
