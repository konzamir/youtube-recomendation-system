# Generated by Django 3.1.1 on 2020-09-24 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_youtubecredentials_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubecredentials',
            name='client_id',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='youtubecredentials',
            name='client_secret',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='youtubecredentials',
            name='expiry',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='youtubecredentials',
            name='refresh_token',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='youtubecredentials',
            name='token',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='youtubecredentials',
            name='token_uri',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
