# Generated by Django 3.2 on 2023-05-16 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_type',
            new_name='role',
        ),
    ]
