# Generated by Django 5.0.6 on 2024-06-16 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0006_user_alter_playlist_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.URLField(null=True),
        ),
    ]
