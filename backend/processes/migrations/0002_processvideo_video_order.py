# Generated by Django 3.1.1 on 2020-10-12 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='processvideo',
            name='video_order',
            field=models.IntegerField(default=None),
        ),
    ]
