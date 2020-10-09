from django.db import models
from userProfile.models import OrgProfile
import uuid
import os

STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive')
)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/sliders', filename)


class Slider(models.Model):
    name = models.CharField(max_length=288, unique=True, null=False, blank=False)
    img = models.ImageField(upload_to=get_file_path, null=False)
    status = models.CharField(max_length=20, null=False, blank=False, default='Inactive', choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

