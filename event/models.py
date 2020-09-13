from django.db import models
from userProfile.models import User

STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive')
)


class EventType(models.Model):
    name = models.CharField(max_length=288, unique=True, null=False, blank=False)
    status = models.CharField(max_length=20, null=False, blank=False, default='Inactive', choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventBranchVenue(models.Model):
    name = models.CharField(max_length=288, unique=True, null=False, blank=False)
    status = models.CharField(max_length=20, null=False, blank=False, default='Inactive', choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


