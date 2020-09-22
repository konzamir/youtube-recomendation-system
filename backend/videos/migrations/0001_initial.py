# Generated by Django 3.1.1 on 2020-09-22 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import videos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('filters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filters.source')),
            ],
        ),
        migrations.CreateModel(
            name='ImagePreview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=256)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etag', models.CharField(max_length=128)),
                ('pub_date', models.DateTimeField()),
                ('video_hash', models.CharField(max_length=64)),
                ('positive_mark_number', models.IntegerField(default=0)),
                ('negative_mark_number', models.IntegerField(default=0)),
                ('image_preview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.imagepreview')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(videos.models.VideoStatusChoices['NOT_CHECKED'], 'Video was not checked'), (videos.models.VideoStatusChoices['QUALITATIVE'], 'Video with high quality'), (videos.models.VideoStatusChoices['NON_QUALITATIVE'], 'Video with low quality')], default=videos.models.VideoStatusChoices['NOT_CHECKED'], max_length=5)),
                ('practical_usage_availability', models.BooleanField()),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.channel')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filters.destination')),
                ('video_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filters.videotype')),
                ('youtube_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.youtubedata')),
            ],
        ),
        migrations.CreateModel(
            name='UserMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information_quality', models.IntegerField()),
                ('medical_practice_quality', models.IntegerField()),
                ('description_quality', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video')),
            ],
        ),
        migrations.CreateModel(
            name='Featured',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video')),
            ],
        ),
    ]