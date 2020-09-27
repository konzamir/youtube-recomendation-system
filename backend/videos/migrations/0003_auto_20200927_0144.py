# Generated by Django 3.1.1 on 2020-09-27 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0001_initial'),
        ('videos', '0002_auto_20200922_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='youtube_id',
            field=models.CharField(default='w', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='channel',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='filters.source'),
        ),
        migrations.AlterField(
            model_name='video',
            name='practical_usage_availability',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='filters.videotype'),
        ),
        migrations.AlterField(
            model_name='youtubedata',
            name='image_preview',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='videos.imagepreview'),
        ),
    ]