from django.contrib import admin
from .models import Room, Booking

admin.site.register(Room)
admin.site.register(Booking)

admin.site.site_header = "Skikkelig Fancy Hotell"