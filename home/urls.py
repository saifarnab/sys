from django.urls import path
from .views import (
    home, org_home
)


urlpatterns = [
    path('', home, name='home'),
    path('org/<pk>', org_home, name='org'),
]