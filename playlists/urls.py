from django.urls import path
from . import views

urlpatterns = [
    path('playlists/', views.playlists, name='playlists'),
    path('profile/', views.profile, name='profile'),
]