from django.test import TestCase, Client
from main.models import Room, Booking
from django.contrib.auth.models import User



#tester Room-model
class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):  # setter opp et testobjekt
        Room.objects.create(room_no='1', available=True, capacity=2, room_type='D')

    # sjekker om dataen blir lagret riktig
    def test_room_no_is_correct(self):  # sjekker at romnr blir 1
        room = Room.objects.get(id=1)
        this_room_no = room.room_no
        self.assertEqual(this_room_no, '1')

    def test_available_is_correct(self):  # sjekker at rommet er ledig
        room = Room.objects.get(id=1)
        is_available = room.available
        self.assertTrue(is_available)

    def test_capacity_is_correct(self):
        room = Room.objects.get(id=1)
        this_room_capacity = room.capacity
        self.assertEqual(this_room_capacity, 2)

    def test_room_type_is_correct(self):
        room = Room.objects.get(id=1)
        this_room_type = room.room_type
        self.assertEqual(this_room_type, 'D')

    #disse sjekker at rommet har blitt opprettet og inneholder alle fields
    def test_room_no(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('room_no').verbose_name  #verbose_name gjør at man får dataen i vanlig leselig versjon (mellomrom osv)
        self.assertEquals(field_label, 'room no')  # bruker assertEquals fordi dersom feil forteller den oss hva labelen egt er

    def test_available(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('available').verbose_name
        self.assertEquals(field_label, 'available')

    def test_capacity(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('capacity').verbose_name
        self.assertEquals(field_label, 'capacity')

    def test_room_type(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('room_type').verbose_name
        self.assertEquals(field_label, 'room type')

    #disse sjekker max lengde
    def test_max_length_room_no(self):
        room = Room.objects.get(id=1)
        max_length = room._meta.get_field('room_no').max_length
        self.assertEquals(max_length, 5)

    def test_max_length_room_type(self):
        room = Room.objects.get(id=1)
        max_length = room._meta.get_field('room_type').max_length
        self.assertEquals(max_length, 1)

# tester Booking-Model
class BookingModelTest(TestCase):
    # oppretter testobjekt
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(username='testuser2')
        test_user.set_password('123password')
        test_room = Room.objects.create(room_no='1', available=True, capacity=2, room_type='D')
        Booking.objects.create(bookingid="1", guest=test_user, cin_date="2020-01-01", cout_date="2020-01-03", room_type="D", room=test_room)

    # disse sjekker at bookingen er blitt opprettet og inneholder alle feltene
    def test_guest(self):
        booking = Booking.objects.get(bookingid="1")
        field_label = booking._meta.get_field('guest').verbose_name
        self.assertEquals(field_label, 'guest')

    def test_cin_date(self):
        booking = Booking.objects.get(bookingid="1")
        field_label = booking._meta.get_field('cin_date').verbose_name
        self.assertEquals(field_label, 'Check-In Date')

    def test_cout_date(self):
        booking = Booking.objects.get(bookingid="1")
        field_label = booking._meta.get_field('cout_date').verbose_name
        self.assertEquals(field_label, 'Check-Out Date')

    def test_room_type(self):
        booking = Booking.objects.get(bookingid="1")
        field_label= booking._meta.get_field('room_type').verbose_name
        self.assertEquals(field_label, 'room type')

    def test_room(self):
        booking = Booking.objects.get(bookingid="1")
        field_label= booking._meta.get_field('room').verbose_name
        self.assertEquals(field_label, 'room')

#tester views
class ViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = Client()

    def test_home_page(self): #tester forsiden
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200) #200 er HTTP OK
        self.assertTemplateUsed(response, "../templates/forside.html")

    #def test_se_rom(self): # tester se_rom-siden
        #response = self.client.get("/se_rom/")
        #self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, "../templates/se_rom.html")

