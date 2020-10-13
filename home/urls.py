from django.urls import path
from .views import (
    home, org_home, event_details, register, login, logout, sub_category_search, org_sub_category_search, save_to_cart
)


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', home, name='home'),
    path('org/<pk>', org_home, name='org'),
    path('event-details/<pk>', event_details, name='event-details'),
    path('sub-category-search/<pk>', sub_category_search, name='sub-category-search'),
    path('org-sub-category-search/<org_id>/<pk>', org_sub_category_search, name='org-sub-category-search'),
    path('save-to-cart/', save_to_cart, name='save-to-cart'),
]