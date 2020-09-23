# Generated by Django 3.1.1 on 2020-09-19 08:44

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20200917_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='content',
            field=ckeditor.fields.RichTextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='duration',
            field=models.CharField(max_length=25),
        ),
    ]