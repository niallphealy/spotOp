from django.contrib import admin
from .models import Playlist, User

# Register your models here.
admin.site.register(Playlist)
admin.site.register(User)