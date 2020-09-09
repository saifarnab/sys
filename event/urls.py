from django.urls import path
from .views import event_list, event_type


urlpatterns = [
    path('', event_list, name='event'),
    path('event-type/', event_type, name='event-type'),
]