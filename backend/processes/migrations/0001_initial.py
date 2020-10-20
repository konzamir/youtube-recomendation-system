# Generated by Django 3.1.1 on 2020-10-20 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('videos', '0001_initial'),
        ('filters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Waiting For Fetching Base Data'), (1, 'Waiting For Fetching Full Data'), (2, 'Waiting For Filtering Data'), (3, 'Success'), (4, 'Invalid')], default=0)),
                ('youtube_video_group', models.CharField(default=None, max_length=64, null=True)),
                ('active', models.BooleanField(default=False)),
                ('search_data', models.TextField()),
                ('invalid_msg', models.CharField(max_length=128, null=True)),
                ('next_process', models.IntegerField(default=None, null=True)),
                ('prev_process', models.IntegerField(default=None, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_order', models.IntegerField(default=None)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pv_processes', to='processes.process')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pv_videos', to='videos.video')),
            ],
            options={
                'unique_together': {('video', 'process')},
            },
        ),
        migrations.CreateModel(
            name='ProcessTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pt_processes', to='processes.process')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pt_tags', to='filters.tag')),
            ],
            options={
                'unique_together': {('tag', 'process')},
            },
        ),
        migrations.CreateModel(
            name='ProcessSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ps_processes', to='processes.process')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ps_sources', to='filters.source')),
            ],
            options={
                'unique_together': {('source', 'process')},
            },
        ),
        migrations.CreateModel(
            name='ProcessCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pc_categories', to='filters.category')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pc_processes', to='processes.process')),
            ],
            options={
                'unique_together': {('category', 'process')},
            },
        ),
    ]
