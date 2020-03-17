from django.test import TestCase, Client
from main.models import Room
from django.urls import reverse



#tester models
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



#tester views
class ViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = Client()

    def test_home_page(self): #tester forsiden
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200) #200 er HTTP OK
        self.assertTemplateUsed(response, "../templates/forside.html")

    def test_se_rom(self): # tester se_rom-siden
        response = self.client.get("/se_rom/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "../templates/se_rom.html")

