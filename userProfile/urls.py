from django.urls import path
from .views import sign_in, sign_out, delete_org, profile, member, org, update_org, delete_member, org_trainer, create_trainer, update_trainer, delete_trainer, update_member

urlpatterns = [
    path('login/', sign_in, name='admin-login'),
    path('logout/', sign_out, name='admin-logout'),
    path('org-trainer/', org_trainer, name='org-trainer'),
    path('admin-org/', org, name='admin-org'),
    path('admin-member/', member, name='admin-member'),
    path('create-org-trainer/', create_trainer, name='create-org-trainer'),
    path('update-org-trainer/<int:pk>', update_trainer, name='update-org-trainer'),
    path('delete-org-trainer/<int:pk>', delete_trainer, name='delete-org-trainer'),
    path('update-admin-member/<int:pk>', update_member, name='update-admin-member'),
    path('delete-admin-member/<int:pk>', delete_member, name='delete-admin-member'),
    path('update-admin-org/<int:pk>', update_org, name='update-admin-org'),
    path('delete-admin-org/<int:pk>', delete_org, name='delete-admin-org'),
    path('admin-profile/', profile, name='admin-profile'),

]