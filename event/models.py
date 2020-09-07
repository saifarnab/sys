from django.db import models


class EventType(models.Model):
    name = models.CharField(max_length=288, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class EventType(models.Model):
#     name = models.CharField(max_length=288, null=False, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)