# Generated by Django 5.0.6 on 2024-06-16 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0002_user_alter_playlist_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='author',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('spotify_id', models.CharField(max_length=255)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlists.playlist')),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
