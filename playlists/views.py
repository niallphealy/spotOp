from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.conf import settings

from .models import Playlist, User
from .forms import PlaylistCreateForm

import requests

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_CLIENT_ID = 'f851e13d067a415ea6a8a56e8f7cf761'
SPOTIFY_CLIENT_SECRET = '1314aa00802c4bf4bcedeee449fc46a7'
SPOTIFY_REDIRECT_URI = 'http://localhost:8000/spotify_callback'

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
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data, headers=headers)
    token_response = response.json()
    
    # Store the access token in session
    if 'access_token' in token_response:
        request.session['spotify_access_token'] = token_response['access_token']
        messages.success(request, "Successfully authenticated with Spotify.")
    else:
        messages.error(request, "Failed to authenticate with Spotify.")
    
    return redirect('playlists:profile')

def index(request):
   template = loader.get_template("index.html")
   return HttpResponse(template.render({}, request))

def playlists(request):
    playlists = Playlist.objects.all().values()
    template = loader.get_template("myfirst.html")
    return HttpResponse(template.render({"playlists": playlists}, request) )

def profile(request):
    # Use the stored access token to make Spotify API requests
    if 'spotify_access_token' in request.session:
        access_token = request.session['spotify_access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        profile_data = response.json()

        if request.method == "POST":
            form = PlaylistCreateForm(request.POST)
            print(request.POST)
            print(form)
            if form.is_valid():
                print("success")

                playlist_id = request.POST["playlist_link"][34:-20]
                create_playlist_resp = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers={'Authorization': f'Bearer {request.session["spotify_access_token"]}'})
                if create_playlist_resp.status_code == 200:
                    create_playlist_resp = create_playlist_resp.json()
                    if create_playlist_resp["owner"]["id"] != profile_data["id"]:
                        raise Exception("You do not own this playlist")

                    name = create_playlist_resp["name"]
                    uri = playlist_id
                    author = User.objects.get(pk=create_playlist_resp["owner"]["id"])
                    picture = create_playlist_resp["images"][0]["url"]

                    Playlist.objects.create(name=name, uri=uri, author=author, picture=picture)
                    return redirect("playlists:profile")
                else:
                    raise Exception("Playlist not found")
        else:
            form = PlaylistCreateForm()
        

        user, created = User.objects.get_or_create(username=profile_data["id"], defaults={"name": profile_data["display_name"], "picture": profile_data["images"][1]["url"]})

        print(f"The user {user.name} was {None if created else 'not'} created")


        
        context = {"user": user, "playlists": Playlist.objects.filter(author=user.username), "form": form}
        return render(request, "profile.html", context)
    else:
        return render(request, "profile.html")

def playlist(request, playlist_id):
    if "spotify_access_token" in request.session:
        playlist_response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers={'Authorization': f'Bearer {request.session["spotify_access_token"]}'})
        print(playlist_response)
        if playlist_response.status_code != 200:
            raise Exception("Error fetching playlist")
        playlist_data = playlist_response.json()
        # context = {"name": playlist_data["name"], "author": playlist_data["owner"]["id"]}

 
    return render(request, "playlist.html", context={"playlist_id":playlist_id})