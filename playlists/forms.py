from django import forms
from .models import User, Playlist

class PlaylistCreateForm(forms.Form):
    playlist_link = forms.CharField(max_length=255, label="playlist_link")
