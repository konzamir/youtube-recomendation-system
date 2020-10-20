# Generated by Django 3.1.1 on 2020-10-20 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_id', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=4)),
                ('description', models.TextField()),
                ('keywords', models.TextField()),
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
                ('video_hash', models.CharField(max_length=64, unique=True)),
                ('positive_mark_number', models.IntegerField(default=0)),
                ('negative_mark_number', models.IntegerField(default=0)),
                ('view_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('image_preview', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='videos.imagepreview')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Not Checked'), (1, 'Checked')], default=0)),
                ('practical_usage_availability', models.BooleanField(null=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='filters.category')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.channel')),
                ('youtube_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='videos.youtubedata')),
            ],
        ),
        migrations.CreateModel(
            name='UserMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information_quality', models.IntegerField(null=True)),
                ('medical_practice_quality', models.IntegerField(null=True)),
                ('description_quality', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='um_user', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='um_videos', to='videos.video')),
            ],
            options={
                'unique_together': {('video', 'user')},
            },
        ),
        migrations.CreateModel(
            name='TagVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tv_tags', to='filters.tag')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tv_videos', to='videos.video')),
            ],
            options={
                'unique_together': {('video', 'tag')},
            },
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
            options={
                'unique_together': {('video', 'user')},
            },
        ),
        migrations.CreateModel(
            name='ChannelSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cs_channel', to='videos.channel')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cs_sources', to='filters.source')),
            ],
            options={
                'unique_together': {('source', 'channel')},
            },
        ),
    ]
