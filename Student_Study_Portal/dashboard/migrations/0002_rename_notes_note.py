# Generated by Django 5.0 on 2023-12-26 02:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notes',
            new_name='Note',
        ),
    ]
