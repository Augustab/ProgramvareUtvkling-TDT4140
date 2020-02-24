from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect
from . models import Room

# Create your views here.

##denne var bare for å teste
def index(response):
    return HttpResponse("<h1>NY ENDRING</h1>")

##denne må vi ha, den tegner selve forsiden.
def home(response):
    return render(response, "../templates/forside.html")

##denne må vi ha, den tegner se_rom.
def se_rom(response):
    list_of_rooms = Room.objects.all()
    context = {'list_of_rooms': list_of_rooms}
    return render(response, "../templates/se_rom.html", context)

##Denne funksjonen sørger for at dersom du ikke har skrevet noe i url-en (dvs = "http://127.0.0.1:8000/") så skal du redirectes til http://127.0.0.1:8000/home/ dette fordi vi vil at brukerene skal være på hjem siden når man starter programmet.
def redirect(request):
    return HttpResponsePermanentRedirect(reverse('home'))
