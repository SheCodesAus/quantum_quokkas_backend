# Generated by Django 5.1.5 on 2025-01-16 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0004_rename_archive_id_notes_archive_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notes',
            old_name='archive',
            new_name='archive_details',
        ),
        migrations.RenameField(
            model_name='workshop',
            old_name='archive',
            new_name='archive_details',
        ),
    ]
