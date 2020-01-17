# Generated by Django 3.0.2 on 2020-01-10 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherRoomControl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffdataset',
            name="User's First Name",
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffdataset',
            name="User's Last Name",
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffdataset',
            name="User's Middle Name",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
