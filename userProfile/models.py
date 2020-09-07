from django.db import models
from django.contrib.auth.models import AbstractUser


PROFILE_STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive')
)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('Org', 'Org'),
        ('Member', 'Member'),
        ('Trainer', 'Trainer'),
        ('Admin', 'Admin')
    )
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, null=True)


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrgProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=288, unique=True, null=False, blank=False)
    contact_number = models.CharField(max_length=288, null=False, blank=False)
    email = models.CharField(max_length=288, null=False, blank=False)
    address = models.CharField(max_length=288, null=False, blank=False)
    facebook_link = models.CharField(max_length=588, null=False, blank=False)
    twitter_link = models.CharField(max_length=588, null=False, blank=False)
    linkedin_link = models.CharField(max_length=588, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)