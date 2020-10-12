from django.db import models
from ckeditor.fields import RichTextField
from userProfile.models import OrgProfile, TrainerProfile
import uuid
import os

STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive')
)

EVENT_STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive')
)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/events', filename)


class EventType(models.Model):
    name = models.CharField(max_length=288, unique=True, null=False, blank=False)
    status = models.CharField(max_length=20, null=False, blank=False, default='Inactive', choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventBranchVenue(models.Model):
    user = models.ForeignKey(OrgProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=288, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    email = models.CharField(max_length=288, null=True, blank=True)
    contact_no = models.CharField(max_length=288, null=True, blank=True)
    status = models.CharField(max_length=20, null=False, blank=False, default='Inactive', choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventCategory(models.Model):
    name = models.CharField(max_length=288, unique=True, null=False, blank=False)
    status = models.CharField(max_length=20, null=False, blank=False, default='Inactive', choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventSubCategory(models.Model):
    name = models.CharField(max_length=288, unique=True, null=False, blank=False)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, null=False, blank=False, default='Inactive', choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Event(models.Model):
    org = models.ForeignKey(OrgProfile, on_delete=models.CASCADE)
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=288, null=False, blank=False)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(EventSubCategory, on_delete=models.CASCADE)
    starting_date = models.DateField(null=False, blank=False)
    last_registration_date = models.DateField(null=False, blank=False)
    duration = models.CharField(max_length=25, null=False, blank=False)
    session_per_week = models.PositiveIntegerField(null=False, blank=False)
    session_start_time = models.TimeField(null=False, blank=False)
    session_end_time = models.TimeField(null=False, blank=False)
    thumbnail = models.ImageField(upload_to=get_file_path, null=False)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    branch_venue = models.ForeignKey(EventBranchVenue, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    content = RichTextField()
    status = models.CharField(max_length=20, null=False, blank=False, default='Inactive', choices=EVENT_STATUS)
    featured = models.BooleanField(default=False, null=True, blank=True)
    top_rated = models.BooleanField(default=False, null=True, blank=True)
    most_popular = models.BooleanField(default=False, null=True, blank=True)
    best_sell = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



