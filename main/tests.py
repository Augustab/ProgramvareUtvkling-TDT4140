from django.test import TestCase
from main.models import Room

#feil i test_room_no() og test_room_type

class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):  # setter opp et testobjekt
        Room.objects.create(room_no='1', available=True, capacity=2, room_type='D')

    def test_room_no(self):  # sjekker romnr
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('room_no').verbose_name  # verbose_name er verdien i field labelen, her romnr
        self.assertEquals(field_label, 'room_no')  # bruker assertEquals fordi dersom feil forteller den oss hva labelen egt er

    def test_available(self):  # sjekker at rommet er ledig
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
        self.assertEquals(field_label, 'room_type')

    def test_max_length_room_no(self):
        room = Room.objects.get(id=1)
        max_length = room._meta.get_field('room_no').max_length
        self.assertEquals(max_length, 5)

    def test_max_length_room_type(self):
        room = Room.objects.get(id=1)
        max_length = room._meta.get_field('room_type').max_length
        self.assertEquals(max_length, 1)

