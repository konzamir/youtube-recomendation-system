# Generated by Django 3.1.1 on 2020-09-25 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200924_2358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youtubecredentials',
            name='state',
        ),
    ]
