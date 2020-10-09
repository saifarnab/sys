from django.urls import path
from .views import (
    slider,
    create_slider,
    update_slider,
    delete_slider
)


urlpatterns = [
    path('', slider, name='slider'),
    path('create-slider', create_slider, name='create-slider'),
    path('update-slider/<pk>', update_slider, name='update-slider'),
    path('delete-slider/<pk>', delete_slider, name='delete-slider'),
]