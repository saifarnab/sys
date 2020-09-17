from django.urls import path
from .views import (
    video,
    create_video,
    update_video,
    delete_video
)


urlpatterns = [
    path('', video, name='video'),
    path('create-video', create_video, name='create-video'),
    path('update-video/<pk>', update_video, name='update-video'),
    path('delete-video/<pk>', delete_video, name='delete-video'),
]