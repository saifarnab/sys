from django.urls import path
from .views import orgEventConfirm, updateOrgEventConfirm, deleteOrgEventConfirm


urlpatterns = [
    path('', orgEventConfirm, name='org-event-confirm'),
    path('update/<pk>', updateOrgEventConfirm, name='update-org-event-confirm'),
    path('delete/<pk>', deleteOrgEventConfirm, name='delete-org-event-confirm')
]