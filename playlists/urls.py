from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name='index'),
    path('playlists/', views.playlists, name='playlists'),
    path('profile/', views.profile, name='profile'),
    path("login/", views.spotify_login, name="login"),
    path("spotify_callback/", views.spotify_callback, name="spotify_callback"),
    path("playlist/<str:playlist_id>", views.playlist, name="playlist"),
]