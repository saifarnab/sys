from django.urls import path
from .views import event_list


urlpatterns = [
    path('type/', event_list, name='events'),
]