# Generated by Django 3.1.1 on 2020-11-05 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='session_per_week',
        ),
    ]
