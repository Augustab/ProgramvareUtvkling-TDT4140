from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_choices = [('S', 'Single Occupancy'), ('D', 'Double Occupancy'),('B', 'Both Single and Double Occupancy')]

    room_no = models.CharField(max_length=5) #primary key
    available = models.BooleanField(default=False)
    capacity = models.IntegerField(default=None)
    room_type = models.CharField(choices=room_choices, max_length=1, default=None)

