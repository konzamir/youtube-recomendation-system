# Generated by Django 3.1.1 on 2020-09-27 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0001_initial'),
        ('videos', '0003_auto_20200927_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='filters.destination'),
        ),
    ]