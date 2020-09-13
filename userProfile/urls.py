from django.urls import path
from .views import sign_in, sign_out

urlpatterns = [
    path('', sign_in, name='login'),
    path('logout/', sign_out, name='logout')
]