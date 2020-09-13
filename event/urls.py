from django.urls import path
from .views import (
    event_list,
    event_type,
    create_event_type,
    update_event_type,
    delete_event_type,
    event_branch_venue,
    create_event_branch_venue
)


urlpatterns = [
    path('', event_list, name='event'),
    path('event-type/', event_type, name='event-type'),
    path('create-event-type/', create_event_type, name='create-event-type'),
    path('update-event-type/<pk>', update_event_type, name='update-event-type'),
    path('delete-event-type/<pk>', delete_event_type, name='delete-event-type'),
    path('event-branch-venue/', event_branch_venue, name='event-branch-venue'),
    path('create-event-branch-venue/', create_event_branch_venue, name='create-event-branch-venue'),

]