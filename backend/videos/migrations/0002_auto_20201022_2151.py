# Generated by Django 3.1.1 on 2020-10-22 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='practical_usage_availability',
        ),
        migrations.AddField(
            model_name='usermark',
            name='practical_usage_availability',
            field=models.IntegerField(default=0),
        ),
    ]
