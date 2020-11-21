from django.contrib import admin
from .models import Cart, Confirm


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'created_at', 'updated_at']


class ConfirmAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'status', 'created_at', 'updated_at']


admin.site.register(Cart, CartAdmin)
admin.site.register(Confirm, ConfirmAdmin)