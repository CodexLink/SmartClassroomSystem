# Generated by Django 3.0.3 on 2020-02-12 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SCControlSystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroomactionlog',
            name='TimeRecorded',
            field=models.DateTimeField(auto_now_add=True, help_text="Refers to a time from where the log recorded someone's actions.", null=True, verbose_name='Log Action Recorded Time'),
        ),
    ]