# Generated by Django 4.2.5 on 2023-09-23 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_lecture_remove_timetable_class_instance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='description',
        ),
    ]
