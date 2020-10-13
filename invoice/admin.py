from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'created_at', 'updated_at']


admin.site.register(Cart, CartAdmin)