from django.urls import path
from .views import (
    event_type,
    create_event_type,
    update_event_type,
    delete_event_type,
    event_branch_venue,
    create_event_branch_venue,
    update_event_branch_venue,
    delete_event_branch_venue,
    event_category,
    create_event_category,
    update_event_category,
    delete_event_category,
    event_sub_category,
    create_event_sub_category,
    update_event_sub_category,
    delete_event_sub_category,
    get_event_sub_category,  # method for sub cat ajax call
    event,
    create_event,
    update_event,
    delete_event
)

urlpatterns = [

    path('event-type/', event_type, name='event-type'),
    path('create-event-type/', create_event_type, name='create-event-type'),
    path('update-event-type/<pk>', update_event_type, name='update-event-type'),
    path('delete-event-type/<pk>', delete_event_type, name='delete-event-type'),

    path('event-branch-venue/', event_branch_venue, name='event-branch-venue'),
    path('create-event-branch-venue/', create_event_branch_venue, name='create-event-branch-venue'),
    path('update-event-branch-venue/<pk>', update_event_branch_venue, name='update-event-branch-venue'),
    path('delete-event-branch-venue/<pk>', delete_event_branch_venue, name='delete-event-branch-venue'),

    path('event-category/', event_category, name='event-category'),
    path('create-event-category/', create_event_category, name='create-event-category'),
    path('update-event-category/<pk>', update_event_category, name='update-event-category'),
    path('delete-event-category/<pk>', delete_event_category, name='delete-event-category'),
    path('get-sub-cat/<pk>', get_event_sub_category, name='get-sub-cat'),  # method for sub cat ajax call

    path('event-sub-category/', event_sub_category, name='event-sub-category'),
    path('create-event-sub-category/', create_event_sub_category, name='create-event-sub-category'),
    path('update-event-sub-category/<pk>', update_event_sub_category, name='update-event-sub-category'),
    path('delete-event-sub-category/<pk>', delete_event_sub_category, name='delete-event-sub-category'),

    path('event/', event, name='event'),
    path('create-event/', create_event, name='create-event'),
    path('update-event/<pk>', update_event, name='update-event'),
    path('delete-event/<pk>', delete_event, name='delete-event'),

]
