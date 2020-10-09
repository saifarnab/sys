from django.contrib import admin
from .models import Slider


class SliderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'img', 'created_at', 'updated_at', 'status']


admin.site.register(Slider, SliderAdmin)