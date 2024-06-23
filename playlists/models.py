from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    picture = models.URLField(null=True)

    def __str__(self):
        return self.name



class Playlist(models.Model):
    name = models.CharField(max_length=255)
    uri = models.CharField(max_length=255, primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.URLField(null=True)

    def __str__(self):
        return self.name

# class Song(models.Model):
#     name = models.CharField(max_length=255)
#     spotify_id = models.CharField(max_length=255)
#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

 