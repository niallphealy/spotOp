from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.conf import settings
from .models import Playlist, User
import requests

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_CLIENT_ID = 'your_client_id'
SPOTIFY_CLIENT_SECRET = 'your_client_secret'
SPOTIFY_REDIRECT_URI = 'http://yourdomain.com/spotify/callback'

def spotify_login(request):
    # Redirect users to Spotify authorization endpoint
    authorize_url = f"{SPOTIFY_AUTH_URL}?client_id={SPOTIFY_CLIENT_ID}&redirect_uri={SPOTIFY_REDIRECT_URI}&response_type=code"
    return redirect(authorize_url)

def spotify_callback(request):
    code = request.GET.get('code')
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)
    token_response = response.json()
    
    # Store the access token in session
    if 'access_token' in token_response:
        request.session['spotify_access_token'] = token_response['access_token']
        messages.success(request, "Successfully authenticated with Spotify.")
    else:
        messages.error(request, "Failed to authenticate with Spotify.")
    
    return redirect('spotify:index')

def index(request):
    # Use the stored access token to make Spotify API requests
    if 'spotify_access_token' in request.session:
        access_token = request.session['spotify_access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        # Example: Make API request to get user's profile
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        profile_data = response.json()
        return render(request, 'spotify/index.html', {'profile': profile_data})
    else:
        return render(request, 'spotify/index.html')

def playlists(request):
    playlists = Playlist.objects.all().values()
    template = loader.get_template("myfirst.html")
    return HttpResponse(template.render({"playlists": playlists}, request) )

def profile(request):
    # Use the stored access token to make Spotify API requests
    template = loader.get_template("profile.html")
    if 'spotify_access_token' in request.session:
        access_token = request.session['spotify_access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        # Example: Make API request to get user's profile
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        profile_data = response.json()
        # if user exists, update all user data with up-to-date info
        try:
            user = User.objects.get(pk=profile_data["id"])
        # otherwise, create a new user
        except:
            user = User(name=profile_data["display_name"], username=profile_data["id"], picture=profile_data["images"][0]["url"])
    
        setattr(user, "name", profile_data["display_name"])
        setattr(user, "picture", profile_data["images"][0]["url"])
        context = {"user": user, "playlists": Playlist.objects.filter(author=user["username"])}
        return render(request, template, context)
    else:
        return render(request, template)

    # user = User.objects.all().values()[0]
    # playlists = Playlist.objects.filter(author=user["username"])
    # context = {"user": user, "playlists": playlists}
    # template = loader.get_template("profile.html")
    # return HttpResponse( template.render(context, request) )