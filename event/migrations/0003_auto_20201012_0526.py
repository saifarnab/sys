# Generated by Django 3.1.1 on 2020-10-12 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20201012_0340'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventbranchvenue',
            name='email',
            field=models.CharField(blank=True, max_length=288, null=True),
        ),
        migrations.AlterField(
            model_name='eventbranchvenue',
            name='contact_no',
            field=models.CharField(blank=True, max_length=288, null=True),
        ),
    ]