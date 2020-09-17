from django.urls import path
from .views import (
    banner,
    create_banner,
    update_banner,
    delete_banner
)


urlpatterns = [
    path('', banner, name='banner'),
    path('create-banner', create_banner, name='create-banner'),
    path('update-banner/<pk>', update_banner, name='update-banner'),
    path('delete-banner/<pk>', delete_banner, name='delete-banner'),
]