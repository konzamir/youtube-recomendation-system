# Generated by Django 3.1.1 on 2020-10-06 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20201006_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
