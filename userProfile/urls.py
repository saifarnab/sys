from django.urls import path
from .views import sign_in, sign_out, org_trainer, create_trainer, update_trainer, delete_trainer

urlpatterns = [
    path('login/', sign_in, name='admin-login'),
    path('logout/', sign_out, name='admin-logout'),
    path('org-trainer/', org_trainer, name='org-trainer'),
    path('create-org-trainer/', create_trainer, name='create-org-trainer'),
    path('update-org-trainer/<int:pk>', update_trainer, name='update-org-trainer'),
    path('delete-org-trainer/<int:pk>', delete_trainer, name='delete-org-trainer')
]