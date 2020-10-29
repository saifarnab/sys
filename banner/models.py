from django.db import models
from userProfile.models import OrgProfile
import uuid
import os

STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive')
)


class Banner(models.Model):
    user = models.ForeignKey(OrgProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=288, unique=True, null=False, blank=False)
    img = models.ImageField(upload_to='banners/', null=False)
    status = models.CharField(max_length=20, null=False, blank=False, default='Inactive', choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

