# Generated by Django 5.0.6 on 2024-06-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0007_user_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='picture',
            field=models.URLField(null=True),
        ),
    ]