from django.urls import path
from .views import (
    home, org_home, event_details, register, login
)


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', home, name='home'),
    path('org/<pk>', org_home, name='org'),
    path('event-details/<pk>', event_details, name='event-details'),
]