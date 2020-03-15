from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    room_choices = [('S', 'Single Occupancy'), ('D', 'Double Occupancy'), ('F', 'Firemannsrom')]
    room_no = models.CharField(max_length=5)  # primary key
    available = models.BooleanField(default=False)
    capacity = models.IntegerField(default=None)
    room_type = models.CharField(choices=room_choices, max_length=1, default=None)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Romnr: " + str(self.room_no) + " -- type:" + str(self.room_type)


class Booking(models.Model):
    #defaultRom = Room.objects.get(room_no='100')
    #defaultRomID = defaultRom.id
    room_choices = [('S', 'Single Occupancy'), ('D', 'Double Occupancy'), ('F', 'Firemannsrom')]
    bookingid = models.AutoField(db_column='BookingID', primary_key=True)  # Field name made lowercase.
    guest = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # eller settings.AUTH_USER_MODEL
    cin_date = models.DateField(db_column='CIN_Date', blank=True, null=True,
                                    verbose_name='Check-In Date')  # Field name made lowercase.
    cout_date = models.DateField(db_column='COUT_Date', blank=True, null=True,
                                     verbose_name='Check-Out Date')  # Field name made lowercase.
    room_type = models.CharField(choices=room_choices, max_length=1, default=None)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, db_column='Room', default=None)

    class Meta:
        managed = True
        db_table = 'Booking'

    def __str__(self):
        return "Bruker: " + self.guest.__str__() + " -- id:" + str(self.bookingid) + " -- Inndato: " +  self.cin_date.__str__() + " -- Utdato: " + self.cout_date.__str__() + " -- " + self.room.__str__()
