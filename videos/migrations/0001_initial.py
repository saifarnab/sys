# Generated by Django 3.1.1 on 2020-09-17 03:19

from django.db import migrations, models
import django.db.models.deletion
import videos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userProfile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=288, unique=True)),
                ('video', models.ImageField(upload_to=videos.models.get_file_path)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userProfile.orgprofile')),
            ],
        ),
    ]
