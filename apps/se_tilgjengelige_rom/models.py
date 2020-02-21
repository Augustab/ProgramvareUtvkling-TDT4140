from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_choices = [('S', 'Single Occupancy'), ('D', 'Double Occupancy'),('B', 'Both Single and Double Occupancy')]

    room_no = models.CharField(max_length=5)
    available = models.BooleanField(default=False)
    capacity = models.IntegerField(default=None)
    room_type = models.CharField(choices=room_choices, max_length=1, default=None)

'''
class Guest(models.Model):
    user = models.OneToOneField(User,default=None, null=True, on_delete=models.CASCADE)

    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(choices=gender_choices,max_length=1, default=None, null=True)

    username = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=20, blank=False)
    realname = models.CharField(max_length=30, blank=True)

    room_allotted = models.BooleanField(default=False)
    rooms_booked = models.ForeignKey(Room, related_name='entries', blank=False, on_delete=models.CASCADE
    )

    class Meta:
        managed = True
        db_table = 'Guest'


class Admin(models.Model):
    user = models.OneToOneField(User,default=None, null=True, on_delete=models.CASCADE)

    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(choices=gender_choices,max_length=1, default=None, null=True)

    username = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=20, blank=False)
    realname = models.CharField(max_length=30, blank=True)

    class Meta:
        managed = True
        db_table = 'Admin'


class Cleaner(models.Model):
    user = models.OneToOneField(User,default=None, null=True, on_delete=models.CASCADE)

    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(choices=gender_choices,max_length=1, default=None, null=True)

    username = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=20, blank=False)
    realname = models.CharField(max_length=30, blank=True)

    class Meta:
        managed = True
        db_table = 'Cleaner'


class Booking(models.Model):
    bookingid = models.AutoField(db_column='BookingID', primary_key=True)  # Field name made lowercase.
    admin = models.ForeignKey(Admin, models.DO_NOTHING, db_column='Admin_ID' ,default='1')  # Field name made lowercase.
    customer = models.ForeignKey('Customer', models.DO_NOTHING, db_column='Customer_ID',default='1')  # Field name made lowercase.
    cin_date = models.DateTimeField(db_column='CIN_Date', blank=True, null=True,verbose_name='Check-In Date')  # Field name made lowercase.
    cout_date = models.DateTimeField(db_column='COUT_Date', blank=True, null=True, verbose_name='Check-Out Date')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Booking'
'''