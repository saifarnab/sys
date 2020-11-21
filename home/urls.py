from django.urls import path
from .views import (
    home, org_home, event_details, register, login, logout, sub_category_search,
    org_sub_category_search, save_to_cart, user_cart, delete_event_from_cart, user_profile,
    home_search, trainer_profile, register_as_org, confirm_event
)


urlpatterns = [
    path('register/', register, name='register'),
    path('register-org/', register_as_org, name='register-org'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('user-profile/', user_profile, name='user-profile'),
    path('trainer-profile/<int:pk>', trainer_profile, name='trainer-profile'),
    path('', home, name='home'),
    path('org/<pk>', org_home, name='org'),
    path('event-details/<pk>', event_details, name='event-details'),
    path('sub-category-search/<pk>', sub_category_search, name='sub-category-search'),
    path('org-sub-category-search/<org_id>/<pk>', org_sub_category_search, name='org-sub-category-search'),
    path('save-to-cart/', save_to_cart, name='save-to-cart'),
    path('cart/', user_cart, name='cart'),
    path('delete-cart/<int:pk>', delete_event_from_cart, name='delete-cart'),
    path('home-search/', home_search, name='home-search'),
    path('confirm-event/<int:pk>', confirm_event, name='confirm-event'),
]