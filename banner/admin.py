from django.contrib import admin
from .models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'img', 'created_at', 'updated_at', 'status']


admin.site.register(Banner, BannerAdmin)