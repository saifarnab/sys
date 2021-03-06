# Generated by Django 3.1.1 on 2020-10-29 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=288, unique=True)),
                ('img', models.ImageField(upload_to='sliders/')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
