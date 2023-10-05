# Generated by Django 4.2.5 on 2023-10-05 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0010_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable.section'),
        ),
        migrations.AlterField(
            model_name='section',
            name='section_type',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
